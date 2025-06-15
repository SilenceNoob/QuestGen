import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from functools import wraps
from dotenv import load_dotenv
from config import config
from document_processor import DocumentProcessor
from question_generator import QuestionGenerator
from scorer import Scorer
from session_manager import FileSessionManager

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置应用
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# 设置session为永久性
from datetime import timedelta
app.permanent_session_lifetime = timedelta(seconds=app.config.get('PERMANENT_SESSION_LIFETIME', 3600))

# 全局题目配置文件路径
QUESTION_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'question_config.json')

# 默认题目配置
DEFAULT_QUESTION_CONFIG = {
    'single_choice': 5,
    'multiple_choice': 3,
    'true_false': 2,
    'thinking': 0
}

def load_question_config():
    """加载全局题目配置"""
    try:
        if os.path.exists(QUESTION_CONFIG_FILE):
            with open(QUESTION_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载题目配置失败: {e}")
    return DEFAULT_QUESTION_CONFIG.copy()

def save_question_config(config_data):
    """保存全局题目配置"""
    try:
        with open(QUESTION_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存题目配置失败: {e}")
        return False

# 初始化组件
doc_processor = DocumentProcessor(app.config['UPLOAD_FOLDER'])
question_generator = QuestionGenerator(
    app.config['DEEPSEEK_API_KEY'],
    app.config['DEEPSEEK_API_URL']
)
scorer = Scorer(app.config['SCORING'], question_generator)

# 使用文件系统存储会话数据，支持容器重启后的数据持久化
session_manager = FileSessionManager(
    session_dir='sessions',
    timeout=app.config.get('PERMANENT_SESSION_LIFETIME', 3600)
)

# 认证装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('需要管理员权限才能访问此页面', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_available_documents():
    """获取所有可用的文档列表"""
    documents = []
    upload_folder = app.config['UPLOAD_FOLDER']
    if os.path.exists(upload_folder):
        for filename in os.listdir(upload_folder):
            if filename.startswith('.'):  # 跳过隐藏文件
                continue
            filepath = os.path.join(upload_folder, filename)
            if os.path.isfile(filepath):
                documents.append({
                    'filename': filename,
                    'original_name': filename,  # 现在文件名保留中文，直接使用
                    'size': os.path.getsize(filepath)
                })
    return documents

@app.route('/')
def index():
    """首页"""
    # 获取可用文档列表供普通用户选择
    documents = get_available_documents()
    return render_template('index.html', documents=documents)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """管理员登录"""
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in app.config['ADMIN_USERS'] and app.config['ADMIN_USERS'][username] == password:
        session.permanent = True  # 设置为永久session
        session['is_admin'] = True
        session['admin_username'] = username
        flash('登录成功', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('用户名或密码错误', 'error')
        return render_template('login.html')

@app.route('/logout')
def logout():
    """登出"""
    session.pop('is_admin', None)
    session.pop('admin_username', None)
    flash('已成功登出', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """管理员仪表板"""
    documents = get_available_documents()
    return render_template('admin.html', documents=documents)

@app.route('/admin/delete_document', methods=['POST'])
@admin_required
def delete_document():
    """删除文档"""
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'success': False, 'error': '缺少文件名参数'})
    
    filename = data['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': '文件不存在'})
    
    try:
        os.remove(filepath)
        return jsonify({'success': True, 'message': f'文档 {filename} 已删除'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'删除失败: {str(e)}'})

@app.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload_document():
    """文档上传页面（仅管理员）"""
    if request.method == 'GET':
        return render_template('upload.html')
    
    # 处理文件上传
    if 'document' not in request.files:
        return jsonify({'success': False, 'error': '请选择文件'})
    
    file = request.files['document']
    if file.filename == '':
        return jsonify({'success': False, 'error': '请选择文件'})
    
    # 检查文件格式
    if not doc_processor.allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'success': False, 'error': '文件格式不支持'})
    
    # 检查是否需要覆盖确认
    force_overwrite = request.form.get('force_overwrite', 'false').lower() == 'true'
    if not force_overwrite and doc_processor.check_file_exists(file.filename):
        return jsonify({
            'success': False, 
            'error': 'file_exists',
            'message': f'文件 "{file.filename}" 已存在，是否要覆盖？',
            'filename': file.filename
        })
    
    # 保存文件
    filepath = doc_processor.save_uploaded_file(file, app.config['ALLOWED_EXTENSIONS'])
    if not filepath:
        return jsonify({'success': False, 'error': '文件上传失败'})
    
    # 只返回上传成功信息，不进行文档解析
    return jsonify({
        'success': True,
        'message': f'文档 "{file.filename}" 上传成功！',
        'filename': file.filename
    })

@app.route('/select_documents', methods=['POST'])
def select_documents():
    """选择已有文档生成题目"""
    data = request.get_json()
    if not data or 'selected_documents' not in data:
        return jsonify({'success': False, 'error': '请选择至少一个文档'})
    
    selected_files = data['selected_documents']
    if not selected_files:
        return jsonify({'success': False, 'error': '请选择至少一个文档'})
    
    # 读取选中文档的内容
    combined_content = ""
    document_info = []
    total_word_count = 0
    
    for filename in selected_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': f'文档 {filename} 不存在'})
        
        # 提取文档内容
        result = doc_processor.extract_text(filepath)
        if result['success']:
            combined_content += f"\n\n=== {result['filename']} ===\n\n" + result['content']
            document_info.append({
                'filename': result['filename'],
                'word_count': result['word_count']
            })
            total_word_count += result['word_count']
        else:
            return jsonify({'success': False, 'error': f'无法读取文档 {filename}: {result.get("error", "未知错误")}'})
    
    # 生成会话ID
    import uuid
    session_id = str(uuid.uuid4())
    session.permanent = True  # 设置为永久session
    session['session_id'] = session_id
    
    # 存储文档内容
    session_data = {
        'document_content': combined_content,
        'document_info': {
            'filename': f"已选择 {len(selected_files)} 个文档",
            'word_count': total_word_count,
            'selected_documents': document_info
        },
        'is_from_selection': True
    }
    session_manager.set(session_id, session_data)
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'document_info': session_data['document_info']
    })

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    """生成题目"""
    session_id = session.get('session_id')
    if not session_id or not session_manager.exists(session_id):
        return jsonify({'success': False, 'error': '会话已过期，请重新选择文档或上传文档'})
    
    session_data = session_manager.get(session_id)
    if not session_data:
        return jsonify({'success': False, 'error': '会话数据丢失，请重新选择文档或上传文档'})
    
    # 使用全局题目配置
    question_config = load_question_config()
    
    # 验证配置
    total_questions = sum(question_config.values())
    if total_questions == 0:
        return jsonify({'success': False, 'error': '题目配置错误，请联系管理员设置题目数量'})
    if total_questions > 20:
        return jsonify({'success': False, 'error': '题目配置错误，总数超过20道，请联系管理员调整'})
    
    # 生成题目
    document_content = session_data['document_content']
    result = question_generator.generate_questions(document_content, question_config)
    
    # 校验各题型数量，若不足则报错
    if result['success']:
        questions = result['questions']
        from collections import Counter
        type_counter = Counter([q.get('type') for q in questions])
        missing_types = []
        for qtype, count in question_config.items():
            if count > 0 and type_counter.get(qtype, 0) < count:
                missing_types.append(qtype)
        if missing_types:
            return jsonify({'success': False, 'error': f'题目生成异常，以下题型数量不足：{','.join(missing_types)}，请重试或联系管理员减少题目数量'})
        # 存储生成的题目
        session_data['questions'] = questions
        session_data['question_config'] = question_config
        session_manager.set(session_id, session_data)
        return jsonify({
            'success': True,
            'questions': questions,
            'total_count': result['total_count']
        })
    else:
        return jsonify(result)

@app.route('/config')
def config_questions():
    """题目配置页面"""
    session_id = session.get('session_id')
    if not session_id or not session_manager.exists(session_id):
        flash('会话已过期，请重新选择文档', 'error')
        return redirect(url_for('index'))
    
    session_data = session_manager.get(session_id)
    if not session_data:
        flash('会话数据丢失，请重新选择文档', 'error')
        return redirect(url_for('index'))
    
    document_info = session_data['document_info']
    
    return render_template('config.html', document_info=document_info)

@app.route('/quiz')
def quiz():
    """答题页面"""
    session_id = session.get('session_id')
    if not session_id or not session_manager.exists(session_id):
        flash('会话已过期，请重新上传文档', 'error')
        return redirect(url_for('index'))
    
    session_data = session_manager.get(session_id)
    if not session_data:
        flash('会话数据丢失，请重新上传文档', 'error')
        return redirect(url_for('index'))
    
    if 'questions' not in session_data:
        flash('请先生成题目', 'error')
        return redirect(url_for('config_questions'))
    
    questions = session_data['questions']
    document_info = session_data['document_info']
    
    return render_template('quiz.html', 
                         questions=questions, 
                         document_info=document_info)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    """提交答案并评分"""
    session_id = session.get('session_id')
    if not session_id or not session_manager.exists(session_id):
        return jsonify({'success': False, 'error': '会话已过期，请重新上传文档'})
    
    session_data = session_manager.get(session_id)
    if not session_data:
        return jsonify({'success': False, 'error': '会话数据丢失，请重新上传文档'})
    
    if 'questions' not in session_data:
        return jsonify({'success': False, 'error': '题目不存在，请重新生成'})
    
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'success': False, 'error': '答案数据格式错误'})
    
    user_answers = data['answers']
    questions = session_data['questions']
    
    # 验证答案格式
    validation = scorer.validate_answers(questions, user_answers)
    if not validation['valid']:
        return jsonify({
            'success': False, 
            'error': '答案格式错误',
            'details': validation['errors']
        })
    
    # 计算分数
    score_result = scorer.calculate_score(questions, user_answers)
    
    # 存储结果
    session_data['score_result'] = score_result
    session_data['user_answers'] = user_answers
    session_manager.set(session_id, session_data)
    
    return jsonify({
        'success': True,
        'score_result': score_result
    })

@app.route('/result')
def result():
    """结果页面"""
    session_id = session.get('session_id')
    if not session_id or not session_manager.exists(session_id):
        flash('会话已过期，请重新上传文档', 'error')
        return redirect(url_for('index'))
    
    session_data = session_manager.get(session_id)
    if not session_data:
        flash('会话数据丢失，请重新上传文档', 'error')
        return redirect(url_for('index'))
    
    if 'score_result' not in session_data:
        flash('请先完成答题', 'error')
        return redirect(url_for('quiz'))
    
    score_result = session_data['score_result']
    document_info = session_data['document_info']
    
    # 获取统计信息
    statistics = scorer.get_statistics(score_result['results'])
    
    return render_template('result.html', 
                         score_result=score_result,
                         document_info=document_info,
                         statistics=statistics)

@app.route('/restart')
def restart():
    """重新开始"""
    session_id = session.get('session_id')
    if session_id and session_manager.exists(session_id):
        session_data = session_manager.get(session_id)
        if session_data:
            # 只清理上传的文件，不清理选择的文档
            if 'filepath' in session_data and not session_data.get('is_from_selection', False):
                doc_processor.cleanup_file(session_data['filepath'])
        
        # 清理会话数据
        session_manager.delete(session_id)
    
    # 保留管理员登录状态
    is_admin = session.get('is_admin')
    admin_username = session.get('admin_username')
    session.clear()
    if is_admin:
        session['is_admin'] = is_admin
        session['admin_username'] = admin_username
    
    return redirect(url_for('index'))

@app.route('/session_status')
def session_status():
    """检查会话状态"""
    session_id = session.get('session_id')
    if not session_id or not session_manager.exists(session_id):
        return jsonify({'valid': False})
    
    data = session_manager.get(session_id)
    if not data:
        return jsonify({'valid': False})
    
    status = {
        'valid': True,
        'has_document': 'document_content' in data,
        'has_questions': 'questions' in data,
        'has_results': 'score_result' in data
    }
    
    return jsonify(status)

@app.route('/question_config')
@admin_required
def question_config():
    """题目配置页面（仅管理员）"""
    config = load_question_config()
    return render_template('question_config.html', config=config)

@app.route('/save_question_config', methods=['POST'])
@admin_required
def save_question_config_route():
    """保存题目配置（仅管理员）"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '请求数据格式错误'})
        
        # 验证配置数据
        config = {
            'single_choice': int(data.get('single_choice', 0)),
            'multiple_choice': int(data.get('multiple_choice', 0)),
            'true_false': int(data.get('true_false', 0)),
            'thinking': int(data.get('thinking', 0))
        }
        
        # 验证数值范围（使用新的限制配置）
        type_limits = {
            'single_choice': 10,
            'multiple_choice': 8,
            'true_false': 10,
            'thinking': 5
        }
        
        type_names = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'thinking': '思考题'
        }
        
        for key, value in config.items():
            if value < 0:
                return jsonify({'success': False, 'error': f'{type_names.get(key, key)}数量不能为负数'})
            if value > type_limits.get(key, 20):
                return jsonify({'success': False, 'error': f'{type_names.get(key, key)}数量不能超过{type_limits.get(key, 20)}道'})
        
        # 验证总数
        total = sum(config.values())
        if total == 0:
            return jsonify({'success': False, 'error': '请至少设置一种题型的数量'})
        if total > app.config.get('MAX_TOTAL_QUESTIONS', 20):
            return jsonify({'success': False, 'error': f'题目总数不能超过{app.config.get("MAX_TOTAL_QUESTIONS", 20)}道'})
        
        # 保存配置
        if save_question_config(config):
            return jsonify({'success': True, 'message': '配置保存成功'})
        else:
            return jsonify({'success': False, 'error': '配置保存失败'})
            
    except ValueError:
        return jsonify({'success': False, 'error': '配置数据格式错误'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'保存失败: {str(e)}'})

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# 清理函数
def cleanup_old_sessions():
    """清理过期的会话数据（可以通过定时任务调用）"""
    # 这里可以实现基于时间的会话清理逻辑
    pass

if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 检查API密钥
    if not app.config['DEEPSEEK_API_KEY']:
        print("警告: DEEPSEEK_API_KEY 环境变量未设置")
        print("请设置环境变量: export DEEPSEEK_API_KEY='your-api-key'")
    
    # 根据配置设置调试模式和端口
    debug_mode = app.config.get('DEBUG', False)
    port = int(os.environ.get('APP_PORT', 5000))
    
    app.run(debug=debug_mode, port=port, host='0.0.0.0')