import json
import requests
from typing import Dict, List, Any, Optional
import re

class QuestionGenerator:
    """题目生成器，调用DeepSeek API生成题目"""
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    
    def generate_questions(self, document_content: str, question_config: Dict[str, int]) -> Dict[str, Any]:
        """生成题目"""
        if not self.api_key:
            return {'success': False, 'error': 'DeepSeek API密钥未配置'}
        
        try:
            # 构建prompt
            prompt = self._build_prompt(document_content, question_config)
            
            # 调用API
            response = self._call_deepseek_api(prompt)
            
            if not response['success']:
                return response
            
            # 解析返回的题目
            questions = self._parse_questions(response['content'])
            
            if not questions:
                return {'success': False, 'error': '题目解析失败，请重试'}
            
            return {
                'success': True,
                'questions': questions,
                'total_count': len(questions)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'题目生成失败: {str(e)}'}
    
    def _build_prompt(self, content: str, config: Dict[str, int]) -> str:
        """构建API请求的prompt"""
        total_questions = sum(config.values())
        
        prompt = f"""请基于以下文档内容生成{total_questions}道题目：

文档内容：
{content[:3000]}  # 限制内容长度避免token过多

要求：
1. 生成{config.get('single_choice', 0)}道单选题，{config.get('multiple_choice', 0)}道多选题，{config.get('true_false', 0)}道判断题
2. 题目要准确反映文档内容，不能脱离文档内容
3. 单选题提供4个选项（A、B、C、D），多选题提供4个选项（可选择多个），判断题只需要对错判断
4. 选项要有一定迷惑性但答案必须明确且正确
5. 题目难度适中，适合理解性测试

请严格按照以下JSON格式返回，不要添加任何其他内容：
{{
  "questions": [
    {{
      "type": "single_choice",
      "question": "题目内容",
      "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
      "correct_answer": "A",
      "explanation": "答案解释"
    }},
    {{
      "type": "multiple_choice",
      "question": "题目内容",
      "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
      "correct_answer": ["A", "C"],
      "explanation": "答案解释"
    }},
    {{
      "type": "true_false",
      "question": "题目内容",
      "options": ["A. 正确", "B. 错误"],
      "correct_answer": "A",
      "explanation": "答案解释"
    }}
  ]
}}"""
        
        return prompt
    
    def _call_deepseek_api(self, prompt: str) -> Dict[str, Any]:
        """调用DeepSeek API"""
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return {'success': True, 'content': content}
            else:
                error_msg = f"API调用失败，状态码: {response.status_code}"
                if response.text:
                    error_msg += f"，错误信息: {response.text}"
                return {'success': False, 'error': error_msg}
                
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'API调用超时，请重试'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'网络请求失败: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'API调用异常: {str(e)}'}
    
    def _parse_questions(self, content: str) -> List[Dict[str, Any]]:
        """解析API返回的题目内容"""
        try:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                if 'questions' in data and isinstance(data['questions'], list):
                    questions = []
                    for i, q in enumerate(data['questions']):
                        if self._validate_question(q):
                            q['id'] = i + 1
                            questions.append(q)
                    return questions
            
            return []
            
        except json.JSONDecodeError:
            # 如果JSON解析失败，尝试其他解析方法
            return self._fallback_parse(content)
        except Exception:
            return []
    
    def _validate_question(self, question: Dict[str, Any]) -> bool:
        """验证题目格式是否正确"""
        required_fields = ['type', 'question', 'options', 'correct_answer']
        
        # 检查必需字段
        for field in required_fields:
            if field not in question:
                return False
        
        # 检查题目类型
        if question['type'] not in ['single_choice', 'multiple_choice', 'true_false']:
            return False
        
        # 检查选项格式
        if not isinstance(question['options'], list) or len(question['options']) == 0:
            return False
        
        # 检查答案格式
        if question['type'] == 'multiple_choice':
            if not isinstance(question['correct_answer'], list):
                return False
        else:
            if not isinstance(question['correct_answer'], str):
                return False
        
        return True
    
    def _fallback_parse(self, content: str) -> List[Dict[str, Any]]:
        """备用解析方法"""
        # 这里可以实现更复杂的文本解析逻辑
        # 暂时返回空列表，实际使用中可以根据需要完善
        return []
    
    def get_question_summary(self, questions: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取题目统计信息"""
        summary = {
            'single_choice': 0,
            'multiple_choice': 0,
            'true_false': 0,
            'total': len(questions)
        }
        
        for question in questions:
            q_type = question.get('type')
            if q_type in summary:
                summary[q_type] += 1
        
        return summary