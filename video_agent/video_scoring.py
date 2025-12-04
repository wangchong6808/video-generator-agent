from typing import Dict
from volcenginesdkarkruntime import Ark
from agent_base.utils import parse_response
from loguru import logger
import json


class VideoScoringTool:
    """视频评分工具"""
    
    def __init__(self, client: Ark):
        """
        初始化视频评分工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"
    
    def score(self, prompt: str, video_url: str) -> Dict:
        """
        为生成的视频打分
        
        Args:
            prompt: 生成视频时使用的提示词
            video_url: 生成的视频URL
            
        Returns:
            包含视频评分和反馈的字典，格式：{"score": "85", "feedback": "..."}
        """
        score_prompt_template = """
你是一个专业的视频质量评估专家，负责评估生成的视频是否符合给定的提示词要求。

请仔细分析视频与提示词的匹配度，评估以下方面：
1. 主题相关性：视频内容与提示词的匹配程度
2. 画面质量：清晰度、色彩、构图等
3. 动态效果：流畅度、动作自然度
4. 整体观感：是否符合预期，视觉吸引力

请使用以下JSON格式返回评估结果：
{
    "score": "{{分数}}", // 字符串 0-100之间，例如 "85"
    "feedback": "{{反馈内容}}" // 简短的反馈描述
}
        """

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": score_prompt_template}],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_video",
                            "video_url": video_url,
                            "fps": 1,
                        }
                    ],
                },
            ],
            store=True,
        )

        parsed_response = parse_response(response)
        response_message = "".join(parsed_response["message"])
        logger.info(f"Video Scoring Response: {response_message}")

        try:
            return json.loads(response_message)
        except json.JSONDecodeError:
            # 如果返回格式不符合要求，返回默认评分
            return {
                "score": "60",
                "feedback": "评分工具返回格式异常，使用默认评分"
            }
