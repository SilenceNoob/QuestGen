from typing import Dict, List, Any

class Scorer:
    """评分器，处理答案对比和评分计算"""
    
    def __init__(self, scoring_config: Dict[str, int], question_generator=None):
        self.scoring_config = scoring_config
        self.question_generator = question_generator
    
    def calculate_score(self, questions: List[Dict[str, Any]], user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """计算总分和详细结果"""
        results = []
        total_score = 0
        max_score = 0
        correct_count = 0
        
        for question in questions:
            question_id = str(question['id'])
            question_type = question['type']
            correct_answer = question['correct_answer']
            user_answer = user_answers.get(question_id, None)
            
            # 计算单题分数
            question_score = self.scoring_config.get(question_type, 0)
            max_score += question_score
            
            # 判断答案是否正确
            if question_type == 'thinking':
                # 思考题使用AI评估
                ai_result = self._evaluate_thinking_question(
                    question['question'], 
                    correct_answer, 
                    user_answer, 
                    question.get('explanation', '')
                )
                is_correct = ai_result.get('is_correct', False)
                # 思考题按比例计分
                earned_score = int(question_score * ai_result.get('score', 0) / 100)
                if ai_result.get('score', 0) >= 60:
                    correct_count += 1
            else:
                # 其他题型使用传统方法
                is_correct = self._check_answer(question_type, correct_answer, user_answer)
                if is_correct:
                    earned_score = question_score
                    correct_count += 1
                else:
                    earned_score = 0
            
            total_score += earned_score
            
            # 记录详细结果
            result_detail = {
                'question_id': question['id'],
                'question': question['question'],
                'question_type': question_type,
                'options': question['options'],
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'is_correct': is_correct,
                'earned_score': earned_score,
                'max_score': question_score,
                'explanation': question.get('explanation', '')
            }
            
            # 为思考题添加AI评估详情
            if question_type == 'thinking' and 'ai_result' in locals():
                result_detail.update({
                    'ai_score': ai_result.get('score', 0),
                    'ai_feedback': ai_result.get('feedback', ''),
                    'key_points_covered': ai_result.get('key_points_covered', []),
                    'suggestions': ai_result.get('suggestions', '')
                })
            
            results.append(result_detail)
        
        # 计算百分比分数
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        return {
            'total_score': total_score,
            'max_score': max_score,
            'percentage': round(percentage, 1),
            'correct_count': correct_count,
            'total_questions': len(questions),
            'accuracy': round(correct_count / len(questions) * 100, 1) if questions else 0,
            'results': results,
            'grade': self._get_grade(percentage)
        }
    
    def _evaluate_thinking_question(self, question: str, reference_answer: str, user_answer: str, explanation: str) -> Dict[str, Any]:
        """评估思考题答案"""
        if not self.question_generator:
            # 如果没有question_generator，使用简单的文本匹配评估
            if not user_answer or not user_answer.strip():
                return {
                    'score': 0,
                    'feedback': '未提供答案',
                    'is_correct': False
                }
            
            # 简单的关键词匹配评估
            user_lower = user_answer.lower()
            ref_lower = reference_answer.lower()
            
            # 计算简单的相似度
            common_words = set(user_lower.split()) & set(ref_lower.split())
            if len(common_words) >= 2:
                score = min(80, len(common_words) * 20)
            elif len(user_answer.strip()) >= 50:  # 至少有一定长度的回答
                score = 60
            else:
                score = 30
            
            return {
                'score': score,
                'feedback': f'基于关键词匹配的评估，匹配到{len(common_words)}个关键词',
                'is_correct': score >= 60
            }
        
        # 使用AI评估
        return self.question_generator.evaluate_thinking_answer(
            question, reference_answer, user_answer, explanation
        )
    
    def _check_answer(self, question_type: str, correct_answer: Any, user_answer: Any) -> bool:
        """检查答案是否正确"""
        if user_answer is None:
            return False
        
        if question_type == 'multiple_choice':
            # 多选题：用户答案和正确答案都应该是列表
            if not isinstance(user_answer, list) or not isinstance(correct_answer, list):
                return False
            
            # 排序后比较，确保顺序不影响结果
            user_set = set(user_answer)
            correct_set = set(correct_answer)
            return user_set == correct_set
        
        else:
            # 单选题和判断题：直接比较字符串
            return str(user_answer).strip().upper() == str(correct_answer).strip().upper()
    
    def _get_grade(self, percentage: float) -> str:
        """根据百分比获取等级"""
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """获取答题统计信息"""
        if not results:
            return {}
        
        stats = {
            'by_type': {},
            'difficulty_analysis': {},
            'common_mistakes': []
        }
        
        # 按题型统计
        type_stats = {}
        for result in results:
            q_type = result['question_type']
            if q_type not in type_stats:
                type_stats[q_type] = {'total': 0, 'correct': 0}
            
            type_stats[q_type]['total'] += 1
            if result['is_correct']:
                type_stats[q_type]['correct'] += 1
        
        # 计算各题型正确率
        for q_type, data in type_stats.items():
            accuracy = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            stats['by_type'][q_type] = {
                'total': data['total'],
                'correct': data['correct'],
                'accuracy': round(accuracy, 1)
            }
        
        return stats
    
    def format_answer_display(self, question_type: str, answer: Any) -> str:
        """格式化答案显示"""
        if answer is None:
            return "未作答"
        
        if question_type == 'multiple_choice':
            if isinstance(answer, list):
                return ', '.join(sorted(answer))
            else:
                return str(answer)
        else:
            return str(answer)
    
    def validate_answers(self, questions: List[Dict[str, Any]], user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """验证用户提交的答案格式"""
        errors = []
        warnings = []
        
        for question in questions:
            question_id = str(question['id'])
            question_type = question['type']
            user_answer = user_answers.get(question_id)
            
            if user_answer is None:
                warnings.append(f"题目 {question_id} 未作答")
                continue
            
            # 验证多选题答案格式
            if question_type == 'multiple_choice':
                if not isinstance(user_answer, list):
                    errors.append(f"题目 {question_id} 答案格式错误，多选题答案应为列表")
                elif len(user_answer) == 0:
                    warnings.append(f"题目 {question_id} 未选择任何选项")
            
            # 验证单选题和判断题答案格式
            elif question_type in ['single_choice', 'true_false']:
                if not isinstance(user_answer, str):
                    errors.append(f"题目 {question_id} 答案格式错误，应为字符串")
                elif not user_answer.strip():
                    warnings.append(f"题目 {question_id} 答案为空")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }