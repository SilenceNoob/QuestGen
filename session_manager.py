import os
import json
import time
from typing import Dict, Any, Optional
from threading import Lock

class FileSessionManager:
    """基于文件系统的会话管理器，支持容器重启后的数据持久化"""
    
    def __init__(self, session_dir: str = 'sessions', timeout: int = 3600):
        self.session_dir = session_dir
        # 确保 timeout 是整数（处理可能传入的 timedelta 对象）
        if hasattr(timeout, 'total_seconds'):
            self.timeout = int(timeout.total_seconds())
        else:
            self.timeout = int(timeout)  # 会话超时时间（秒）
        self.lock = Lock()
        
        # 确保会话目录存在
        os.makedirs(session_dir, exist_ok=True)
    
    def _get_session_file(self, session_id: str) -> str:
        """获取会话文件路径"""
        return os.path.join(self.session_dir, f"{session_id}.json")
    
    def _is_session_expired(self, session_file: str) -> bool:
        """检查会话是否过期"""
        try:
            stat = os.stat(session_file)
            return time.time() - stat.st_mtime > self.timeout
        except OSError:
            return True
    
    def set(self, session_id: str, data: Dict[str, Any]) -> bool:
        """设置会话数据"""
        try:
            with self.lock:
                session_file = self._get_session_file(session_id)
                with open(session_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        except Exception as e:
            print(f"保存会话数据失败: {e}")
            return False
    
    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话数据"""
        try:
            with self.lock:
                session_file = self._get_session_file(session_id)
                
                # 检查文件是否存在
                if not os.path.exists(session_file):
                    return None
                
                # 检查是否过期
                if self._is_session_expired(session_file):
                    self.delete(session_id)
                    return None
                
                # 读取数据
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"读取会话数据失败: {e}")
            return None
    
    def delete(self, session_id: str) -> bool:
        """删除会话数据"""
        try:
            with self.lock:
                session_file = self._get_session_file(session_id)
                if os.path.exists(session_file):
                    os.remove(session_file)
                return True
        except Exception as e:
            print(f"删除会话数据失败: {e}")
            return False
    
    def exists(self, session_id: str) -> bool:
        """检查会话是否存在且未过期"""
        session_file = self._get_session_file(session_id)
        return (os.path.exists(session_file) and 
                not self._is_session_expired(session_file))
    
    def cleanup_expired(self) -> int:
        """清理过期的会话文件"""
        cleaned = 0
        try:
            with self.lock:
                for filename in os.listdir(self.session_dir):
                    if filename.endswith('.json'):
                        session_file = os.path.join(self.session_dir, filename)
                        if self._is_session_expired(session_file):
                            os.remove(session_file)
                            cleaned += 1
        except Exception as e:
            print(f"清理过期会话失败: {e}")
        return cleaned
    
    def update(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """更新会话数据"""
        data = self.get(session_id)
        if data is None:
            return False
        
        data.update(updates)
        return self.set(session_id, data)