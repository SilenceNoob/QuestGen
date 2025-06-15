import os
import json
from typing import Dict, Any

class Config:
    """应用程序配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('FLASK_SECRET_KEY') or 'your-secret-key-here'
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = 3600  # 1小时
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # 开发环境设为False，生产环境应设为True
    
    # 管理员账户配置（仅用于内部测试）
    ADMIN_USERS = {
        'admin': os.environ.get('ADMIN_PASSWORD', 'admin123'),  # 用户名: 密码
        'test': 'test123'     # 可以添加多个管理员账户
    }
    
    # DeepSeek API配置 - 在init_app中动态设置
    DEEPSEEK_API_KEY = None
    DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'md'}
    
    # 题目生成配置
    DEFAULT_QUESTION_COUNT = {
        'single_choice': 5,
        'multiple_choice': 3,
        'true_false': 2,
        'thinking': 2  # 思考题
    }
    
    # 题目数量限制配置（防止超出AI上下文限制）
    MAX_QUESTIONS_PER_TYPE = {
        'single_choice': 10,
        'multiple_choice': 8,
        'true_false': 10,
        'thinking': 5  # 思考题限制较少，因为容易超出上下文
    }
    
    # 总题目数量限制
    MAX_TOTAL_QUESTIONS = 20
    
    # 评分配置
    SCORING = {
        'single_choice': 10,  # 单选题分值
        'multiple_choice': 15,  # 多选题分值
        'true_false': 5,      # 判断题分值
        'thinking': 20        # 思考题分值
    }
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 动态设置SECRET_KEY
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.environ.get('FLASK_SECRET_KEY') or 'your-secret-key-here'
        
        # 动态设置API密钥和其他环境变量配置
        app.config['DEEPSEEK_API_KEY'] = os.environ.get('DEEPSEEK_API_KEY', '')
        app.config['DEEPSEEK_API_URL'] = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1/chat/completions')
        app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
        
        # 设置最大内容长度
        max_content = os.environ.get('MAX_CONTENT_LENGTH')
        if max_content:
            app.config['MAX_CONTENT_LENGTH'] = int(max_content)

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # 开发环境禁用安全cookie

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # 生产环境启用安全cookie

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}