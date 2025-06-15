import os
import re
from typing import Optional, Dict, Any
from werkzeug.utils import secure_filename
from docx import Document
import PyPDF2
import uuid

class DocumentProcessor:
    """文档处理器，支持多种文档格式的文本提取"""
    
    def __init__(self, upload_folder: str = 'uploads'):
        self.upload_folder = upload_folder
        self.ensure_upload_folder()
    
    def ensure_upload_folder(self):
        """确保上传文件夹存在"""
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def allowed_file(self, filename: str, allowed_extensions: set) -> bool:
        """检查文件扩展名是否允许"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    def safe_filename(self, filename: str) -> str:
        """生成安全的文件名，保留中文字符"""
        # 移除危险字符但保留中文
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # 如果文件名为空或只包含点，生成随机文件名
        if not filename or filename.replace('.', '').strip() == '':
            ext = filename.split('.')[-1] if '.' in filename else ''
            filename = f"upload_{uuid.uuid4().hex[:8]}.{ext}" if ext else f"upload_{uuid.uuid4().hex[:8]}"
        return filename
    
    def save_uploaded_file(self, file, allowed_extensions: set) -> Optional[str]:
        """保存上传的文件并返回文件路径"""
        if file and file.filename and self.allowed_file(file.filename, allowed_extensions):
            filename = self.safe_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            return filepath
        return None
    
    def check_file_exists(self, filename: str) -> bool:
        """检查文件是否已存在"""
        filename = self.safe_filename(filename)
        filepath = os.path.join(self.upload_folder, filename)
        return os.path.exists(filepath)
    
    def extract_text_from_txt(self, filepath: str) -> str:
        """从txt文件提取文本"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(filepath, 'r', encoding='gbk') as file:
                    return file.read()
            except:
                with open(filepath, 'r', encoding='latin-1') as file:
                    return file.read()
    
    def extract_text_from_docx(self, filepath: str) -> str:
        """从docx文件提取文本"""
        doc = Document(filepath)
        text_content = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text)
        
        return '\n'.join(text_content)
    
    def extract_text_from_pdf(self, filepath: str) -> str:
        """从PDF文件提取文本"""
        text_content = []
        
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():
                    text_content.append(text)
        
        return '\n'.join(text_content)
    
    def extract_text_from_md(self, filepath: str) -> str:
        """从Markdown文件提取文本"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 移除Markdown语法标记
            # 移除标题标记
            content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
            # 移除粗体和斜体标记
            content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
            content = re.sub(r'\*([^*]+)\*', r'\1', content)
            content = re.sub(r'__([^_]+)__', r'\1', content)
            content = re.sub(r'_([^_]+)_', r'\1', content)
            # 移除链接标记，保留链接文本
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
            # 移除图片标记
            content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', content)
            # 移除代码块标记
            content = re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)
            content = re.sub(r'`([^`]+)`', r'\1', content)
            # 移除引用标记
            content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
            # 移除列表标记
            content = re.sub(r'^[\s]*[-*+]\s+', '', content, flags=re.MULTILINE)
            content = re.sub(r'^[\s]*\d+\.\s+', '', content, flags=re.MULTILINE)
            # 移除水平分割线
            content = re.sub(r'^[-*_]{3,}$', '', content, flags=re.MULTILINE)
            
            return content
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(filepath, 'r', encoding='gbk') as file:
                    return file.read()
            except:
                with open(filepath, 'r', encoding='latin-1') as file:
                    return file.read()
    
    def extract_text(self, filepath: str) -> Dict[str, Any]:
        """根据文件类型提取文本内容"""
        if not os.path.exists(filepath):
            return {'success': False, 'error': '文件不存在'}
        
        try:
            file_ext = os.path.splitext(filepath)[1].lower()
            
            if file_ext == '.txt':
                content = self.extract_text_from_txt(filepath)
            elif file_ext == '.docx':
                content = self.extract_text_from_docx(filepath)
            elif file_ext == '.pdf':
                content = self.extract_text_from_pdf(filepath)
            elif file_ext == '.md':
                content = self.extract_text_from_md(filepath)
            else:
                return {'success': False, 'error': '不支持的文件格式'}
            
            # 清理文本内容
            content = self.clean_text(content)
            
            if not content.strip():
                return {'success': False, 'error': '文档内容为空'}
            
            return {
                'success': True,
                'content': content,
                'word_count': len(content),
                'filename': os.path.basename(filepath)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'文档处理失败: {str(e)}'}
    
    def clean_text(self, text: str) -> str:
        """清理文本内容"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符但保留中文标点
        text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：""''（）()\\[\\]【】]', '', text)
        return text.strip()
    
    def cleanup_file(self, filepath: str) -> bool:
        """清理（删除）指定的文件"""
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"删除文件失败: {e}")
            return False