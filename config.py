import os
from typing import Dict, Any

class Config:
    """应用程序配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # 管理员账户配置（仅用于内部测试）
    ADMIN_USERS = {
        'admin': 'admin123',  # 用户名: 密码
        'test': 'test123'     # 可以添加多个管理员账户
    }
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY') or ''
    DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'md'}
    
    # 题目生成配置
    DEFAULT_QUESTION_COUNT = {
        'single_choice': 5,
        'multiple_choice': 3,
        'true_false': 2
    }
    
    # 评分配置
    SCORING = {
        'single_choice': 10,  # 单选题分值
        'multiple_choice': 15,  # 多选题分值
        'true_false': 5       # 判断题分值
    }
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}