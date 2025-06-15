# 🎯 智能题目生成系统

基于 DeepSeek API 的智能题目生成和答题系统，支持从文档自动生成单选题、多选题、判断题和思考题，并提供在线答题和自动评分功能。

## ✨ 功能特点

### 📄 文档处理
- **多格式支持**：TXT、DOCX、PDF、MD 格式文档
- **智能解析**：自动提取文档内容和结构
- **文档管理**：支持多文档上传、选择和管理
- **内容预览**：上传后可预览文档信息

### 🤖 AI 题目生成
- **分类生成策略**：按题型分别调用 AI，提高生成稳定性
- **智能数量限制**：防止超出 AI 上下文限制
- **专门提示词优化**：针对不同题型使用专门的提示词
- **质量保证**：多重验证确保题目质量

### 📝 多种题型支持
- **单选题**：4个选项，10分/题，最多10道
- **多选题**：4个选项，15分/题，最多8道
- **判断题**：对错判断，5分/题，最多10道
- **思考题**：开放性问答，20分/题，最多5道，支持AI智能评分

### 💻 现代化界面
- **响应式设计**：完美适配桌面端和移动端
- **美观界面**：现代化 UI 设计，用户体验优良
- **实时反馈**：答题进度实时显示
- **智能提示**：操作引导和错误提示

### 👨‍💼 管理员功能
- **文档管理**：上传、删除、查看文档列表
- **题目配置**：全局设置各题型数量
- **用户管理**：管理员登录和权限控制
- **系统监控**：查看系统状态和使用情况

### 📊 智能评分系统
- **自动评分**：选择题和判断题自动评分
- **AI评分**：思考题使用AI进行智能评分和反馈
- **详细分析**：提供题目解析和答案对比
- **统计报告**：分类统计和正确率分析
- **结果导出**：支持打印和保存结果

## 🛠️ 技术栈

### 后端技术
- **Python 3.7+**：主要开发语言
- **Flask 2.3+**：Web 框架
- **Werkzeug 2.3.7**：WSGI 工具库
- **Requests 2.31.0**：HTTP 请求库
- **Gunicorn 21.2.0**：WSGI HTTP 服务器

### 文档处理
- **python-docx 0.8.11**：DOCX 文档解析
- **PyPDF2 3.0.1**：PDF 文档解析
- **内置 Markdown 解析器**：MD 文档支持

### 前端技术
- **HTML5 + CSS3**：现代化界面
- **原生 JavaScript**：交互逻辑
- **响应式设计**：移动端适配
- **CSS Grid + Flexbox**：布局系统

### AI 服务
- **DeepSeek API**：题目生成和智能评分
- **自定义提示词工程**：优化生成质量

## 📋 系统要求

- **Python 3.7+**
- **DeepSeek API 密钥**
- **2GB+ 内存**（推荐）
- **500MB+ 磁盘空间**
- **稳定的网络连接**（用于 API 调用）

## 🚀 快速开始

### 方法一：直接运行（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/your-username/TestGenApp.git
cd TestGenApp

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API 密钥
cp .env.example .env
# 编辑 .env 文件，填入您的 DeepSeek API 密钥

# 4. 运行应用
python app.py
```

### 方法二：使用虚拟环境

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置并运行
cp .env.example .env
python app.py
```

### 🔑 获取 DeepSeek API 密钥

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册账号并完成实名认证
3. 在控制台创建新的 API 密钥
4. 复制密钥到 `.env` 文件中的 `DEEPSEEK_API_KEY`

### 🎯 默认访问信息

- **应用地址**：http://localhost:8000
- **管理员账户**：admin / admin123
- **测试账户**：test / test123

> ⚠️ **安全提醒**：生产环境请务必修改默认密码！

## 📖 使用指南

### 🔐 登录系统

1. **管理员登录**：拥有完整权限，可配置题目参数
2. **普通用户登录**：可上传文档并答题

### 📄 文档上传

**支持格式**：
- **PDF**：自动提取文本内容
- **DOCX**：完整解析 Word 文档
- **Markdown**：支持 .md 文件

**操作步骤**：
1. 点击「选择文件」按钮
2. 选择一个或多个文档（支持批量上传）
3. 系统自动解析并显示文档列表
4. 勾选需要生成题目的文档

### 🎯 智能题目生成

**生成策略**：
- **按题型分类生成**：避免某类题目被遗漏
- **智能数量控制**：根据文档内容自动调整
- **质量保证**：多轮优化确保题目质量

**题型分布**：
- **选择题**：4选1，测试基础知识
- **判断题**：对错判断，验证理解
- **填空题**：关键词填写，考查记忆
- **思考题**：开放性问题，深度思考

### 📝 在线答题

**答题界面**：
- **进度显示**：实时显示答题进度
- **自动保存**：答案实时保存，防止丢失
- **题目导航**：快速跳转到指定题目
- **时间提醒**：可选的答题时间限制

**答题技巧**：
- 仔细阅读题目要求
- 思考题建议详细作答
- 可随时修改已答题目

### 📊 结果分析

**评分机制**：
- **客观题**：自动评分（选择、判断、填空）
- **主观题**：AI 智能评分（思考题）
- **综合评价**：多维度分析答题表现

**结果展示**：
- **总分统计**：各题型得分和总分
- **错题分析**：标注错误题目和正确答案
- **AI 点评**：针对思考题的详细评价
- **改进建议**：基于答题情况的学习建议

## 📁 项目架构

### 目录结构

```
TestGenApp/
├── 📄 app.py                    # Flask 主应用入口
├── ⚙️ config.py                 # 应用配置和默认参数
├── 📋 requirements.txt          # Python 依赖包列表
├── 🔐 .env.example             # 环境变量配置模板
├── 🔐 .env                     # 环境变量配置（需创建）
├── 📊 question_config.json     # 题目生成配置（动态生成）
├── 📁 static/                  # 前端静态资源
│   ├── 🎨 css/
│   │   └── style.css          # 主样式文件（响应式设计）
│   ├── 📱 js/
│   │   └── script.js          # 前端交互逻辑
│   └── 🖼️ images/             # 图片资源
├── 📄 templates/               # Jinja2 HTML 模板
│   ├── base.html             # 基础布局模板
│   ├── index.html            # 首页（文档上传）
│   ├── login.html            # 登录页面
│   ├── config.html           # 管理员配置页面
│   ├── quiz.html             # 在线答题界面
│   └── results.html          # 结果展示页面
├── 📂 uploads/                 # 用户上传文档存储
├── 🧩 components/              # 核心功能模块
│   ├── __init__.py
│   ├── document_processor.py  # 文档解析处理
│   ├── question_generator.py  # AI 题目生成引擎
│   ├── quiz_manager.py       # 答题会话管理
│   └── result_analyzer.py    # 结果分析评分
└── 📖 README.md               # 项目文档
```

### 核心模块说明

#### 🔧 后端核心
- **app.py**：Flask 应用主入口，路由定义和会话管理
- **config.py**：统一配置管理，包含 AI 参数和系统设置
- **components/**：模块化功能组件
  - `document_processor.py`：多格式文档解析（PDF/DOCX/MD）
  - `question_generator.py`：AI 题目生成和优化
  - `quiz_manager.py`：答题流程和状态管理
  - `result_analyzer.py`：智能评分和结果分析

#### 🎨 前端架构
- **响应式设计**：适配桌面端和移动端
- **模块化 CSS**：组件化样式管理
- **原生 JavaScript**：轻量级交互实现
- **渐进式增强**：确保基础功能可用性

#### 📊 数据流程
1. **文档上传** → 解析提取 → 内容预处理
2. **AI 生成** → 分类请求 → 质量优化 → 题目整合
3. **在线答题** → 实时保存 → 状态管理
4. **智能评分** → 结果分析 → 报告生成

## ⚙️ 配置说明

### 🔐 环境变量配置

复制 `.env.example` 为 `.env` 并配置以下变量：

```bash
# ===================
# DeepSeek AI 配置
# ===================
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# ===================
# Flask 应用配置
# ===================
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_super_secret_key_change_in_production

# ===================
# 应用功能配置
# ===================
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB 文件上传限制
SESSION_TIMEOUT=3600         # 会话超时时间（秒）

# ===================
# 管理员账户配置
# ===================
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
TEST_USERNAME=test
TEST_PASSWORD=test123
```

### 📊 题目生成配置

系统支持动态配置题目生成参数，配置文件：`question_config.json`

```json
{
  "default_counts": {
    "multiple_choice": 5,    // 默认选择题数量
    "true_false": 5,        // 默认判断题数量
    "fill_blank": 3,        // 默认填空题数量
    "thinking": 2            // 默认思考题数量
  },
  "max_counts": {
    "multiple_choice": 15,   // 最大选择题数量
    "true_false": 15,       // 最大判断题数量
    "fill_blank": 10,       // 最大填空题数量
    "thinking": 5            // 最大思考题数量
  },
  "scores": {
    "multiple_choice": 2,    // 选择题分值
    "true_false": 1,        // 判断题分值
    "fill_blank": 3,        // 填空题分值
    "thinking": 10           // 思考题分值
  },
  "total_max_questions": 30  // 总题目数量上限
}
```

### 🎯 AI 生成策略配置

在 `config.py` 中可调整 AI 生成参数：

```python
# AI 请求配置
AI_CONFIG = {
    'temperature': 0.7,        # 创造性程度 (0-1)
    'max_tokens': 2000,        # 最大响应长度
    'timeout': 30,             # 请求超时时间
    'retry_times': 3,          # 失败重试次数
    'content_length_limit': 8000  # 文档内容长度限制
}

# 题目质量控制
QUALITY_CONFIG = {
    'min_question_length': 10,   # 题目最小长度
    'max_question_length': 200,  # 题目最大长度
    'enable_content_filter': True, # 启用内容过滤
    'duplicate_check': True      # 启用重复检查
}
```

## 🚀 部署指南

### 🏭 生产环境部署

#### 方法一：传统部署

```bash
# 1. 环境准备
sudo apt update && sudo apt install python3 python3-pip python3-venv nginx

# 2. 创建应用目录
sudo mkdir -p /var/www/testgen
sudo chown $USER:$USER /var/www/testgen
cd /var/www/testgen

# 3. 克隆项目
git clone https://github.com/your-username/TestGenApp.git .

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 6. 配置环境变量
cp .env.example .env
nano .env  # 编辑生产环境配置

# 7. 启动应用
gunicorn -w 4 -b 127.0.0.1:8000 app:app --daemon
```

#### 方法二：Systemd 服务

创建服务文件 `/etc/systemd/system/testgen.service`：

```ini
[Unit]
Description=TestGen Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/testgen
Environment=PATH=/var/www/testgen/venv/bin
ExecStart=/var/www/testgen/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable testgen
sudo systemctl start testgen
```

#### Nginx 反向代理配置

创建 `/etc/nginx/sites-available/testgen`：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /var/www/testgen/static;
        expires 30d;
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/testgen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 🐳 Docker 部署

#### 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建上传目录
RUN mkdir -p uploads

# 设置环境变量
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

#### Docker Compose 部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  testgen:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./question_config.json:/app/question_config.json
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - testgen
    restart: unless-stopped
```

部署命令：
```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 🔒 安全配置

#### SSL/HTTPS 配置

```bash
# 使用 Let's Encrypt 获取免费 SSL 证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### 防火墙配置

```bash
# UFW 防火墙配置
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

#### 环境变量安全

```bash
# 设置文件权限
chmod 600 .env
chown www-data:www-data .env

# 生产环境必须修改的配置
# - SECRET_KEY: 使用强随机密钥
# - ADMIN_PASSWORD: 修改默认管理员密码
# - FLASK_DEBUG: 设置为 False
```

## 🔧 故障排除

### ❗ 常见问题及解决方案

#### 1. API 相关问题

**问题**：API 密钥错误或请求失败
```
Error: Invalid API key or API request failed
```

**解决方案**：
```bash
# 检查 API 密钥配置
cat .env | grep DEEPSEEK_API_KEY

# 测试 API 连接
curl -H "Authorization: Bearer your_api_key" \
     -H "Content-Type: application/json" \
     https://api.deepseek.com/v1/models

# 检查账户余额
# 访问 DeepSeek 控制台查看余额和使用情况
```

#### 2. 文件上传问题

**问题**：文件上传失败或解析错误
```
Error: File upload failed or unsupported format
```

**解决方案**：
```bash
# 检查上传目录权限
ls -la uploads/
sudo chown -R www-data:www-data uploads/
sudo chmod 755 uploads/

# 检查文件大小限制
echo "当前限制: $(python -c 'import config; print(config.MAX_CONTENT_LENGTH)')"

# 支持的文件格式
echo "支持格式: PDF, DOCX, MD"
```

#### 3. 题目生成问题

**问题**：题目生成失败或质量差
```
Error: Question generation failed or low quality
```

**解决方案**：
```bash
# 检查文档内容长度
python -c "
import sys
from components.document_processor import DocumentProcessor
processor = DocumentProcessor()
content = processor.process_file(sys.argv[1])
print(f'文档长度: {len(content)} 字符')
" your_document.pdf

# 调整生成参数
# 编辑 question_config.json 减少题目数量
# 或在 config.py 中调整 AI_CONFIG
```

#### 4. 性能问题

**问题**：应用响应慢或超时
```
Error: Request timeout or slow response
```

**解决方案**：
```bash
# 检查系统资源
top
free -h
df -h

# 调整 Gunicorn 工作进程数
gunicorn -w 8 -b 0.0.0.0:8000 app:app

# 优化 AI 请求参数
# 在 config.py 中减少 max_tokens 或调整 timeout
```

#### 5. 权限问题

**问题**：登录失败或权限不足
```
Error: Authentication failed or insufficient permissions
```

**解决方案**：
```bash
# 检查默认账户配置
cat .env | grep -E "(ADMIN|TEST)_"

# 重置管理员密码
# 编辑 .env 文件中的 ADMIN_PASSWORD

# 清除会话缓存
rm -rf flask_session/
```

### 📊 日志查看和调试

#### 应用日志

```bash
# 实时查看应用日志
tail -f app.log

# 查看错误日志
grep -i error app.log | tail -20

# 查看 API 请求日志
grep -i "deepseek" app.log | tail -10
```

#### 系统服务日志

```bash
# 查看 Systemd 服务日志
journalctl -u testgen -f

# 查看最近的错误
journalctl -u testgen --since "1 hour ago" -p err

# 查看启动日志
journalctl -u testgen --since today
```

#### Web 服务器日志

```bash
# Nginx 访问日志
tail -f /var/log/nginx/access.log

# Nginx 错误日志
tail -f /var/log/nginx/error.log

# 查看特定错误
grep "500\|502\|503\|504" /var/log/nginx/access.log
```

### 🐛 调试模式

#### 开启详细日志

在 `.env` 文件中设置：
```bash
FLASK_DEBUG=True
FLASK_ENV=development
LOG_LEVEL=DEBUG
```

#### Python 调试

```python
# 在代码中添加调试信息
import logging
logging.basicConfig(level=logging.DEBUG)

# 或使用 print 调试
print(f"Debug: {variable_name}")
```

### 🔄 重启服务

```bash
# 重启应用服务
sudo systemctl restart testgen

# 重启 Nginx
sudo systemctl restart nginx

# Docker 环境重启
docker-compose restart

# 完全重新部署
docker-compose down && docker-compose up -d
```

### 📞 获取帮助

如果问题仍未解决，请：

1. **收集错误信息**：完整的错误日志和堆栈跟踪
2. **环境信息**：操作系统、Python 版本、依赖版本
3. **重现步骤**：详细描述问题出现的操作步骤
4. **配置信息**：相关的配置文件内容（隐藏敏感信息）

然后在 GitHub Issues 中提交问题报告。

## 👨‍💻 开发指南

### 🚀 开发环境设置

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/TestGenApp.git
cd TestGenApp
```

#### 2. 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果有开发专用依赖

# 安装代码格式化工具
pip install black flake8 isort pytest
```

#### 3. 配置开发环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑开发配置
echo "FLASK_ENV=development" >> .env
echo "FLASK_DEBUG=True" >> .env
echo "LOG_LEVEL=DEBUG" >> .env
```

### 🏗️ 项目架构

#### 核心组件

```python
# components/document_processor.py
class DocumentProcessor:
    """文档处理器 - 负责解析各种格式文档"""
    
    def process_file(self, file_path: str) -> str:
        """处理文档文件，返回文本内容"""
        pass

# components/question_generator.py  
class QuestionGenerator:
    """题目生成器 - 负责 AI 题目生成"""
    
    def generate_by_type(self, content: str, question_type: str, count: int) -> List[Dict]:
        """按题型生成题目"""
        pass

# components/quiz_manager.py
class QuizManager:
    """答题管理器 - 负责答题流程管理"""
    
    def create_quiz_session(self, questions: List[Dict]) -> str:
        """创建答题会话"""
        pass

# components/result_analyzer.py
class ResultAnalyzer:
    """结果分析器 - 负责评分和分析"""
    
    def analyze_results(self, answers: Dict, questions: List[Dict]) -> Dict:
        """分析答题结果"""
        pass
```

### 🔧 添加新功能

#### 1. 添加新的题型

```python
# 1. 在 config.py 中添加题型配置
QUESTION_TYPES = {
    'multiple_choice': '选择题',
    'true_false': '判断题', 
    'fill_blank': '填空题',
    'thinking': '思考题',
    'new_type': '新题型'  # 新增
}

# 2. 在 question_generator.py 中添加生成逻辑
def generate_new_type_questions(self, content: str, count: int) -> List[Dict]:
    """生成新题型题目"""
    prompt = f"""
    基于以下内容生成 {count} 道新题型题目：
    {content}
    
    要求：
    1. 题目格式：...
    2. 难度适中
    3. 覆盖重点内容
    """
    
    response = self._call_ai_api(prompt)
    return self._parse_questions(response, 'new_type')

# 3. 在 result_analyzer.py 中添加评分逻辑
def score_new_type_question(self, question: Dict, answer: str) -> Dict:
    """评分新题型"""
    # 实现评分逻辑
    pass
```

#### 2. 扩展文档格式支持

```python
# 在 document_processor.py 中添加新格式支持
def process_new_format(self, file_path: str) -> str:
    """处理新格式文档"""
    try:
        # 实现新格式解析逻辑
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 格式转换逻辑
            return self._clean_content(content)
    except Exception as e:
        raise DocumentProcessingError(f"处理新格式文档失败: {e}")

# 在 process_file 方法中添加格式判断
def process_file(self, file_path: str) -> str:
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        return self.process_pdf(file_path)
    elif file_ext == '.docx':
        return self.process_docx(file_path)
    elif file_ext == '.md':
        return self.process_markdown(file_path)
    elif file_ext == '.new':  # 新格式
        return self.process_new_format(file_path)
    else:
        raise UnsupportedFormatError(f"不支持的文件格式: {file_ext}")
```

#### 3. 添加新的 API 路由

```python
# 在 app.py 中添加新路由
@app.route('/api/new_feature', methods=['POST'])
def new_feature_api():
    """新功能 API 接口"""
    try:
        data = request.get_json()
        
        # 参数验证
        if not data or 'required_param' not in data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 业务逻辑
        result = process_new_feature(data)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"新功能处理失败: {e}")
        return jsonify({'error': str(e)}), 500
```

### 📝 代码规范

#### Python 代码规范

```python
# 1. 使用 Type Hints
from typing import List, Dict, Optional, Union

def process_questions(questions: List[Dict[str, Any]]) -> Optional[Dict[str, Union[int, str]]]:
    """处理题目列表
    
    Args:
        questions: 题目列表，每个题目包含题目信息
        
    Returns:
        处理结果字典，包含统计信息
        
    Raises:
        ValueError: 当题目格式不正确时
    """
    pass

# 2. 错误处理
class TestGenError(Exception):
    """应用基础异常类"""
    pass

class DocumentProcessingError(TestGenError):
    """文档处理异常"""
    pass

class QuestionGenerationError(TestGenError):
    """题目生成异常"""
    pass

# 3. 日志记录
import logging

logger = logging.getLogger(__name__)

def risky_operation():
    try:
        # 可能失败的操作
        result = some_operation()
        logger.info(f"操作成功: {result}")
        return result
    except Exception as e:
        logger.error(f"操作失败: {e}", exc_info=True)
        raise
```

#### 前端代码规范

```javascript
// 1. 使用现代 JavaScript
class QuizManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentQuestion = 0;
        this.answers = new Map();
    }
    
    async loadQuestions() {
        try {
            const response = await fetch('/api/questions');
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error);
            }
            
            this.questions = data.questions;
            this.renderQuestion();
        } catch (error) {
            console.error('加载题目失败:', error);
            this.showError('加载题目失败，请重试');
        }
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        this.container.appendChild(errorDiv);
    }
}

// 2. CSS 组件化
/* 使用 BEM 命名规范 */
.quiz-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.quiz-container__question {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.quiz-container__question--current {
    border-left: 4px solid #007bff;
}
```

### 🧪 测试

#### 单元测试

```python
# tests/test_document_processor.py
import pytest
from components.document_processor import DocumentProcessor

class TestDocumentProcessor:
    def setup_method(self):
        self.processor = DocumentProcessor()
    
    def test_process_pdf(self):
        """测试 PDF 文档处理"""
        content = self.processor.process_file('tests/fixtures/sample.pdf')
        assert len(content) > 0
        assert isinstance(content, str)
    
    def test_unsupported_format(self):
        """测试不支持的文件格式"""
        with pytest.raises(UnsupportedFormatError):
            self.processor.process_file('tests/fixtures/sample.xyz')

# 运行测试
# pytest tests/ -v
```

#### 集成测试

```python
# tests/test_api.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_document(client):
    """测试文档上传接口"""
    with open('tests/fixtures/sample.pdf', 'rb') as f:
        response = client.post('/upload', 
                             data={'file': f},
                             content_type='multipart/form-data')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
```

### 🤝 贡献指南

#### 提交代码

```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 代码格式化
black .
isort .
flake8 .

# 3. 运行测试
pytest tests/

# 4. 提交代码
git add .
git commit -m "feat: 添加新功能描述"

# 5. 推送分支
git push origin feature/new-feature

# 6. 创建 Pull Request
```

#### 提交信息规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动

示例：
feat: 添加思考题 AI 评分功能
fix: 修复文档上传大小限制问题
docs: 更新 API 文档
```

## 📄 许可证

本项目采用 **MIT 许可证**，这意味着您可以：

✅ **商业使用** - 可用于商业项目  
✅ **修改** - 可以修改源代码  
✅ **分发** - 可以分发原始或修改后的代码  
✅ **私人使用** - 可以私人使用  
✅ **专利使用** - 提供专利使用权  

❗ **限制条件**：
- 必须包含原始许可证和版权声明
- 作者不承担任何责任

详情请参阅 [LICENSE](LICENSE) 文件。

## 🆘 支持与帮助

### 📚 文档资源

- **项目文档**：本 README 文件
- **API 文档**：`/docs/api.md`（如果有）
- **常见问题**：查看上方故障排除部分
- **示例代码**：`/examples/` 目录

### 🐛 问题反馈

遇到问题时，请按以下步骤操作：

1. **查看文档**：首先查看故障排除部分
2. **搜索 Issues**：在 GitHub Issues 中搜索类似问题
3. **提交 Issue**：如果没有找到解决方案，请提交新的 Issue

**提交 Issue 时请包含**：
- 详细的问题描述
- 错误日志和堆栈跟踪
- 系统环境信息（OS、Python 版本等）
- 重现步骤
- 相关配置文件（隐藏敏感信息）

### 💬 社区交流

- **GitHub Issues**：[项目 Issues 页面](https://github.com/your-username/TestGenApp/issues)
- **GitHub Discussions**：[项目讨论区](https://github.com/your-username/TestGenApp/discussions)
- **邮件支持**：support@example.com

### 🤝 贡献代码

欢迎贡献代码！请参考上方的开发指南：

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

## 📈 更新日志

### 🎉 v2.0.0 (2024-03-01) - 重大更新

**🚀 新功能**
- ✨ **按题型分类生成**：避免 AI 跳过某类题目
- 🧠 **思考题 AI 评分**：智能评价开放性问题
- 👨‍💼 **管理员系统**：完整的后台管理功能
- 📱 **响应式设计**：完美适配移动端
- 🔄 **智能重试机制**：提高生成成功率

**🛠️ 改进优化**
- ⚡ 优化文档解析性能，支持更大文件
- 🎨 全新 UI 设计，提升用户体验
- 🔒 增强安全性，添加输入验证
- 📊 改进结果分析，提供详细反馈

**🐛 问题修复**
- 修复大文件上传超时问题
- 解决特殊字符导致的解析错误
- 修复移动端样式兼容性问题

### v1.5.0 (2024-02-15)

**新增功能**
- 📝 支持 Markdown 文档格式
- 🔧 添加题目生成配置管理
- 📈 增加答题统计分析

**改进**
- 🚀 优化 AI 提示词，提高题目质量
- 💾 改进会话管理，支持断点续答
- 🎯 优化错误处理和用户提示

### v1.2.0 (2024-02-01)

**新增功能**
- ⚙️ 添加管理员配置功能
- 🔢 支持自定义题目数量
- 📋 增加填空题类型

**改进**
- ⚡ 优化文档处理性能
- 📝 增加错误日志记录
- 🎨 改进界面交互体验

### v1.1.0 (2024-01-15)

**新增功能**
- ✅ 增加多选题支持
- 🎨 改进用户界面设计
- 📊 添加答题进度显示

**修复**
- 🐛 修复 PDF 解析中文乱码问题
- 🔧 解决题目生成偶发失败问题

### v1.0.0 (2024-01-01) - 首次发布

**核心功能**
- 📄 支持 PDF、DOCX 文档解析
- 🤖 基于 DeepSeek AI 的题目生成
- 📝 在线答题系统
- 📊 自动评分和结果分析
- 🎯 支持选择题、判断题

---

## 🌟 致谢

感谢以下技术和服务的支持：

- **[DeepSeek](https://www.deepseek.com/)**：提供强大的 AI 能力
- **[Flask](https://flask.palletsprojects.com/)**：优秀的 Python Web 框架
- **[PyPDF2](https://pypdf2.readthedocs.io/)**：PDF 文档处理
- **[python-docx](https://python-docx.readthedocs.io/)**：Word 文档处理

特别感谢所有贡献者和用户的反馈与支持！

---

<div align="center">

**如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！**

[🏠 首页](https://github.com/your-username/TestGenApp) • 
[📖 文档](https://github.com/your-username/TestGenApp/wiki) • 
[🐛 报告问题](https://github.com/your-username/TestGenApp/issues) • 
[💡 功能建议](https://github.com/your-username/TestGenApp/discussions)

</div>

---

**注意**：使用本应用需要有效的 DeepSeek API 密钥，请确保遵守相关服务条款和使用限制。