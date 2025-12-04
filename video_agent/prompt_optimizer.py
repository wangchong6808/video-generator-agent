from typing import Optional
from volcenginesdkarkruntime import Ark


class VideoPromptOptimizer:
    """视频提示词优化工具"""
    
    def __init__(self, client: Ark):
        """
        初始化视频提示词优化工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"
    
    def optimize(self, user_input: str, feedback: str = "") -> str:
        """
        优化视频生成提示词
        
        Args:
            user_input: 用户的原始视频生成需求
            feedback: 视频检查反馈，用于迭代优化
            
        Returns:
            优化后的视频生成提示词
        """
        prompt_template = """
你是一个专业的AI视频提示词工程师，擅长将用户的自然语言需求转换为高质量的视频生成提示词，提示词语言为中文。

请根据用户需求生成详细、精确的视频生成提示词，包含以下要素：
    - 主体内容
    - 场景描述
    - 风格要求
    - 动态效果
    - 光线和色彩
    - 动作描述
    - 场景变化

用户需求：{user_input}

如果有视频检查反馈，请根据反馈优化提示词：{feedback}

请只返回优化后的提示词，不要添加任何其他内容。
        """
        
        prompt = prompt_template.format(user_input=user_input, feedback=feedback)
        
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt
                        }
                    ]
                }
            ],
            store=True
        )
        
        # 提取优化后的提示词
        optimized_prompt = next(
            item for item in response.output if item.type == "message"
        ).content[0].text.strip()
        return optimized_prompt
