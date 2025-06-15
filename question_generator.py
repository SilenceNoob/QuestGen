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
        """生成题目 - 按题型分别请求AI"""
        if not self.api_key:
            return {'success': False, 'error': 'DeepSeek API密钥未配置'}
        
        try:
            all_questions = []
            question_id = 1
            
            # 按题型分别生成
            for question_type, count in question_config.items():
                if count <= 0:
                    continue
                    
                # 限制单次请求的题目数量上限
                max_per_request = self._get_max_questions_per_type(question_type)
                if count > max_per_request:
                    return {
                        'success': False, 
                        'error': f'{self._get_type_name(question_type)}数量不能超过{max_per_request}道，当前配置为{count}道'
                    }
                
                # 生成该题型的题目
                result = self._generate_questions_by_type(document_content, question_type, count)
                
                if not result['success']:
                    return {
                        'success': False,
                        'error': f'生成{self._get_type_name(question_type)}失败: {result["error"]}'
                    }
                
                # 为题目分配ID
                for question in result['questions']:
                    question['id'] = question_id
                    question_id += 1
                
                all_questions.extend(result['questions'])
            
            if not all_questions:
                return {'success': False, 'error': '未生成任何题目，请检查配置'}
            
            return {
                'success': True,
                'questions': all_questions,
                'total_count': len(all_questions)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'题目生成失败: {str(e)}'}
    
    def evaluate_thinking_answer(self, question: str, reference_answer: str, user_answer: str, explanation: str) -> Dict[str, Any]:
        """使用AI评估思考题答案"""
        if not self.api_key:
            return {'success': False, 'error': 'DeepSeek API密钥未配置'}
        
        if not user_answer or not user_answer.strip():
            return {
                'success': True,
                'score': 0,
                'feedback': '未提供答案',
                'is_correct': False
            }
        
        try:
            prompt = f"""请作为一名专业的教师，评估学生对以下思考题的回答：

题目：{question}

参考答案要点：{reference_answer}

评分标准：{explanation}

学生答案：{user_answer}

请按照以下要求进行评估：
1. 评估学生答案是否理解了题目的核心要点
2. 检查答案是否包含了参考答案的关键内容
3. 评估答案的逻辑性和完整性
4. 给出0-100的分数（0分表示完全错误或无关，100分表示完全正确且全面）
5. 提供具体的反馈意见

请严格按照以下JSON格式返回，不要添加任何其他内容：
{{
  "score": 85,
  "feedback": "具体的评价反馈",
  "is_correct": true,
  "key_points_covered": ["要点1", "要点2"],
  "suggestions": "改进建议"
}}"""
            
            response = self._call_deepseek_api(prompt)
            
            if not response['success']:
                return response
            
            # 解析AI评估结果
            try:
                import json
                result = json.loads(response['content'])
                
                # 验证返回格式
                if 'score' not in result or 'feedback' not in result:
                    return {
                        'success': True,
                        'score': 50,  # 默认分数
                        'feedback': '评估结果格式异常，给予中等分数',
                        'is_correct': True
                    }
                
                # 确保分数在合理范围内
                score = max(0, min(100, result.get('score', 50)))
                
                return {
                    'success': True,
                    'score': score,
                    'feedback': result.get('feedback', ''),
                    'is_correct': score >= 60,  # 60分以上算正确
                    'key_points_covered': result.get('key_points_covered', []),
                    'suggestions': result.get('suggestions', '')
                }
                
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试从文本中提取分数
                content = response['content']
                score_match = re.search(r'"score"\s*:\s*(\d+)', content)
                if score_match:
                    score = int(score_match.group(1))
                    return {
                        'success': True,
                        'score': max(0, min(100, score)),
                        'feedback': '答案已评估，但详细反馈解析失败',
                        'is_correct': score >= 60
                    }
                else:
                    return {
                        'success': True,
                        'score': 50,
                        'feedback': '无法解析评估结果，给予中等分数',
                        'is_correct': True
                    }
                    
        except Exception as e:
            return {'success': False, 'error': f'AI评估失败: {str(e)}'}
    
    def _generate_questions_by_type(self, document_content: str, question_type: str, count: int) -> Dict[str, Any]:
        """按题型生成题目"""
        try:
            # 构建该题型的prompt
            prompt = self._build_prompt_by_type(document_content, question_type, count)
            
            # 调用API
            response = self._call_deepseek_api(prompt)
            
            if not response['success']:
                return response
            
            # 解析返回的题目
            questions = self._parse_questions(response['content'])
            
            # 验证题目类型和数量
            valid_questions = [q for q in questions if q.get('type') == question_type]
            
            if len(valid_questions) < count:
                return {
                    'success': False, 
                    'error': f'生成的{self._get_type_name(question_type)}数量不足，期望{count}道，实际{len(valid_questions)}道'
                }
            
            # 只返回需要的数量
            return {
                'success': True,
                'questions': valid_questions[:count]
            }
            
        except Exception as e:
            return {'success': False, 'error': f'生成{self._get_type_name(question_type)}异常: {str(e)}'}
    
    def _build_prompt_by_type(self, content: str, question_type: str, count: int) -> str:
        """构建特定题型的API请求prompt"""
        # 限制文档内容长度，避免超出上下文限制
        max_content_length = 2500
        if len(content) > max_content_length:
            content = content[:max_content_length] + "\n\n[文档内容已截断]\n"
        
        type_descriptions = {
            'single_choice': '单选题提供4个选项（A、B、C、D），只有一个正确答案',
            'multiple_choice': '多选题提供4个选项（A、B、C、D），可以有多个正确答案',
            'true_false': '判断题只需要对错判断，选项为"A. 正确"和"B. 错误"',
            'thinking': '思考题是开放性问题，需要学生基于文档内容进行深入思考和分析，不提供选项'
        }
        
        type_examples = {
            'single_choice': '''{
      "type": "single_choice",
      "question": "题目内容",
      "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
      "correct_answer": "A",
      "explanation": "答案解释"
    }''',
            'multiple_choice': '''{
      "type": "multiple_choice",
      "question": "题目内容",
      "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
      "correct_answer": ["A", "C"],
      "explanation": "答案解释"
    }''',
            'true_false': '''{
      "type": "true_false",
      "question": "题目内容",
      "options": ["A. 正确", "B. 错误"],
      "correct_answer": "A",
      "explanation": "答案解释"
    }''',
            'thinking': '''{
      "type": "thinking",
      "question": "思考题内容",
      "options": [],
      "correct_answer": "参考答案要点",
      "explanation": "评分标准和要点说明"
    }'''
        }
        
        prompt = f"""请基于以下文档内容生成{count}道{self._get_type_name(question_type)}：

文档内容：
{content}

要求：
1. 生成{count}道{self._get_type_name(question_type)}
2. {type_descriptions[question_type]}
3. 题目要准确反映文档内容，不能脱离文档内容
4. 选项要有一定迷惑性但答案必须明确且正确
5. 题目难度适中，适合理解性测试

请严格按照以下JSON格式返回，不要添加任何其他内容：
{{
  "questions": [
    {type_examples[question_type]}
  ]
}}"""
        
        return prompt
    
    def _get_max_questions_per_type(self, question_type: str) -> int:
        """获取每种题型的最大数量限制"""
        # 尝试从配置文件导入限制，如果失败则使用默认值
        try:
            from config import Config
            limits = Config.MAX_QUESTIONS_PER_TYPE
        except (ImportError, AttributeError):
            # 默认限制值
            limits = {
                'single_choice': 10,
                'multiple_choice': 8,
                'true_false': 10,
                'thinking': 5  # 思考题限制较少，因为容易超出上下文
            }
        return limits.get(question_type, 5)
    
    def _get_type_name(self, question_type: str) -> str:
        """获取题型中文名称"""
        names = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'thinking': '思考题'
        }
        return names.get(question_type, question_type)
    
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
        if question['type'] not in ['single_choice', 'multiple_choice', 'true_false', 'thinking']:
            return False
        
        # 检查选项格式（思考题可以没有选项）
        if question['type'] == 'thinking':
            # 思考题可以有空的选项列表
            if not isinstance(question['options'], list):
                return False
        else:
            # 其他题型必须有选项
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
            'thinking': 0,
            'total': len(questions)
        }
        
        for question in questions:
            q_type = question.get('type')
            if q_type in summary:
                summary[q_type] += 1
        
        return summary