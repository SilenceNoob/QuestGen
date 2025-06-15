# 智能题目生成器

基于 DeepSeek API 的智能题目生成和答题系统，支持从文档自动生成单选题、多选题和判断题，并提供在线答题和自动评分功能。

## 功能特点

- 📄 **多格式文档支持**：支持 TXT、DOCX、PDF、MD 格式文档
- 🤖 **AI 智能生成**：基于 DeepSeek API 生成高质量题目
- 📝 **多种题型**：支持单选题、多选题、判断题
- 💻 **在线答题**：美观的 Web 界面，支持实时保存进度
- 📊 **智能评分**：自动评分并提供详细的答题分析
- 🎨 **现代界面**：响应式设计，支持移动端访问
- 💾 **进度保存**：本地存储答题进度，支持断点续答

## 系统要求

- Python 3.7+
- Conda 环境管理器
- DeepSeek API 密钥

## 安装步骤

### 1. 创建 Conda 虚拟环境

```bash
# 创建新的虚拟环境
conda create -n testgen python=3.9

# 激活环境
conda activate testgen
```

### 2. 安装依赖

```bash
# 进入项目目录
cd /Users/zzx/Documents/TestGenApp

# 安装 Python 依赖
pip install -r requirements.txt
```

### 3. 配置 API 密钥

在项目根目录创建 `.env` 文件，添加您的 DeepSeek API 密钥：

```bash
# 创建环境变量文件
echo "DEEPSEEK_API_KEY=your_deepseek_api_key_here" > .env
```

**获取 DeepSeek API 密钥：**
1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 在 API 管理页面创建新的 API 密钥
4. 将密钥复制到 `.env` 文件中

### 4. 运行应用

```bash
# 开发模式运行
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 使用指南

### 1. 上传文档

1. 访问首页，点击「开始使用」
2. 选择或拖拽上传文档文件（支持 TXT、DOCX、PDF）
3. 系统会自动解析文档并显示基本信息

### 2. 配置题目

1. 设置各类题型的数量：
   - **单选题**：每题 2 分
   - **多选题**：每题 3 分
   - **判断题**：每题 1 分
2. 点击「开始生成题目」
3. 等待 AI 生成题目（通常需要 30-60 秒）

### 3. 在线答题

1. 系统跳转到答题页面
2. 逐题作答，支持随时保存进度
3. 实时显示答题进度
4. 完成后点击「提交答案」

### 4. 查看结果

1. 查看总体成绩和等级
2. 分类统计各题型正确率
3. 详细的题目解析和答案对比
4. 支持筛选查看特定类型的题目
5. 可打印结果报告

## 项目结构

```
TestGenApp/
├── app.py                 # Flask 主应用
├── config.py              # 配置文件
├── document_processor.py  # 文档处理模块
├── question_generator.py  # 题目生成模块
├── scorer.py              # 评分模块
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── .env                  # 环境变量（需要创建）
├── uploads/              # 上传文件目录
├── templates/            # HTML 模板
│   ├── index.html        # 首页
│   ├── upload.html       # 上传页面
│   ├── quiz.html         # 答题页面
│   └── result.html       # 结果页面
└── static/               # 静态资源
    ├── css/
    │   └── style.css     # 样式文件
    └── js/
        └── main.js       # JavaScript 文件
```

## 配置说明

### 环境变量

在 `.env` 文件中可配置以下参数：

```bash
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

# Flask 配置
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# 文件上传配置
MAX_CONTENT_LENGTH=10485760  # 10MB

# 题目生成配置
MAX_QUESTIONS_PER_TYPE=20
API_TIMEOUT=60
API_RETRY_TIMES=3
```

### 题目生成参数

可在 `config.py` 中调整以下参数：

- `MAX_QUESTIONS_PER_TYPE`：每种题型最大数量
- `API_TIMEOUT`：API 请求超时时间
- `API_RETRY_TIMES`：API 请求重试次数
- `SINGLE_CHOICE_SCORE`：单选题分值
- `MULTIPLE_CHOICE_SCORE`：多选题分值
- `TRUE_FALSE_SCORE`：判断题分值

## 部署指南

### 生产环境部署

1. **使用 Gunicorn**：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动应用
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

2. **使用 Nginx 反向代理**：

```nginx
server {
    listen 80;
    server_name your_domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias /path/to/TestGenApp/static;
    }
}
```

3. **环境变量配置**：

```bash
# 生产环境配置
export FLASK_ENV=production
export SECRET_KEY=your_production_secret_key
export DEEPSEEK_API_KEY=your_api_key
```

### Docker 部署

#### 快速部署（推荐）

1. **配置环境变量**
   ```bash
   # 复制环境变量模板
   cp .env.example .env
   
   # 编辑 .env 文件，配置您的 API 密钥
   nano .env
   ```

2. **一键部署**
   ```bash
   # 运行部署脚本
   ./deploy.sh
   ```

#### 手动部署

1. **使用 Docker Compose（推荐）**
   ```bash
   # 构建并启动服务
   docker-compose up -d
   
   # 查看日志
   docker-compose logs -f
   
   # 停止服务
   docker-compose down
   ```

2. **使用 Docker 命令**
   ```bash
   # 构建镜像
   docker build -t testgen-app .
   
   # 运行容器
   docker run -d -p 5000:5000 --env-file .env -v $(pwd)/uploads:/app/uploads testgen-app
   ```

#### 生产环境建议

- 使用反向代理（如 Nginx）
- 配置 HTTPS
- 设置日志轮转
- 定期备份数据
- 修改默认管理员密码

## 故障排除

### 常见问题

1. **API 密钥错误**
   - 检查 `.env` 文件中的 API 密钥是否正确
   - 确认 DeepSeek 账户余额充足

2. **文件上传失败**
   - 检查文件格式是否支持（TXT、DOCX、PDF）
   - 确认文件大小不超过 10MB
   - 检查 `uploads` 目录权限

3. **题目生成失败**
   - 检查网络连接
   - 确认文档内容足够生成题目
   - 查看控制台错误日志

4. **页面样式异常**
   - 检查静态文件路径
   - 清除浏览器缓存
   - 确认 CSS/JS 文件完整

### 日志查看

应用日志会输出到控制台，包含详细的错误信息和调试信息。

## 开发指南

### 添加新功能

1. **新增题型**：
   - 修改 `question_generator.py` 中的生成逻辑
   - 更新 `scorer.py` 中的评分规则
   - 调整前端模板和样式

2. **支持新文档格式**：
   - 在 `document_processor.py` 中添加解析器
   - 更新文件类型检查逻辑

3. **自定义评分规则**：
   - 修改 `scorer.py` 中的计分逻辑
   - 调整 `config.py` 中的分值配置

### 代码规范

- 使用 Python PEP 8 代码规范
- 添加适当的注释和文档字符串
- 进行充分的错误处理
- 编写单元测试

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 支持

如有问题或建议，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至开发者
- 查看项目文档

## 更新日志

### v1.0.0 (2024-01-XX)

- 初始版本发布
- 支持基本的题目生成和答题功能
- 实现文档上传和解析
- 添加在线答题界面
- 完成自动评分系统

---

**注意**：使用本应用需要有效的 DeepSeek API 密钥，请确保遵守相关服务条款和使用限制。