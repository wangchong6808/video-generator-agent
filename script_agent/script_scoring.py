from typing import Dict
from volcenginesdkarkruntime import Ark
from agent_base.utils import parse_response
from loguru import logger
import json


class ScriptScoringTool:
    """剧本打分工具"""
    
    def __init__(self, client: Ark):
        """
        初始化剧本打分工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"
    
    def score(self, script_content: str) -> Dict:
        """
        为生成的剧本打分，评估其是否符合传统剧本格式和质量要求
        
        Args:
            script_content: 生成的剧本内容
            
        Returns:
            包含剧本评分和反馈的字典
        """
        score_prompt_template = """
你是一个专业的剧本评审专家，负责评估生成的剧本是否符合传统剧本格式和质量要求。

请从以下几个维度评估剧本质量（每个维度满分10分）：
1. 格式规范：是否符合传统剧本格式要求
2. 情节完整性：核心情节是否完整
3. 人物塑造：角色是否鲜明，对话是否符合角色性格
4. 场景描述：场景描写是否清晰，有助于理解剧情
5. 动作设计：动作描述是否合理，符合剧情发展
6. 整体结构：剧本结构是否清晰，逻辑是否连贯

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
                            "type": "input_text",
                            "text": f"剧本内容: {script_content}",
                        },
                    ],
                },
            ],
            store=True,
        )

        parsed_response = parse_response(response)
        response_message = "".join(parsed_response["message"])
        # logger.info(f"剧本评分结果: {response_message}")

        try:
            return json.loads(response_message)
        except json.JSONDecodeError:
            # 如果返回格式不符合要求，返回默认评分
            return {
                "score": "60",
                "feedback": "评分工具返回格式异常，使用默认评分"
            }
