from typing import Dict
from volcenginesdkarkruntime import Ark
from agent_base.utils import parse_response
from loguru import logger
import json



class ImageScoringTool:
    """图片检查工具"""

    def __init__(self, client: Ark):
        """
        初始化图片检查工具

        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"

    def score(self, prompt: str, image_url: str) -> Dict:
        """
        检查图片是否符合提示词要求

        Args:
            prompt: 图片生成提示词
            image_url: 生成的图片URL

        Returns:
            包含检查结果的字典，格式如下：
            {
                "符合要求": bool,
                "具体问题": str,
                "改进建议": str
            }
        """
        score_prompt_template = """
你是一个专业的图片质量检查员，负责检查生成的图片是否符合给定的提示词要求。

请仔细分析图片与提示词的匹配度，检查以下方面：
1. 主体内容是否与提示词一致
2. 场景描述是否符合提示词要求
3. 风格是否与提示词匹配
4. 细节是否符合提示词描述
5. 光线和色彩是否符合要求
6. 构图是否符合要求



请使用以下JSON格式返回检查结果：
{
    "评分": {{分数}}, // 整数 0-100之间，例如 80
    "具体问题": {{详细问题描述}}, //分数低于60需要有此项内容
    "改进建议": {{具体改进建议}} //分数低于60需要有此项内容
}
        """

        # score_prompt = score_prompt_template.format(prompt=prompt, image_url=image_url)

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
                            "type": "input_image",
                            "image_url": image_url,
                        },
                        {
                            "type": "input_text",
                            "text": "提示词：{}".format(prompt),
                        },
                    ],
                },
            ],
            store=True,
        )

        parsed_response = parse_response(response)
        response_message = "".join(parsed_response["message"])
        logger.info("Image Scoring Response: {}", response_message)


        return json.loads(response_message)

    def _parse_score_result(self, result_text: str) -> Dict:
        """
        解析图片检查结果

        Args:
            result_text: 检查结果文本

        Returns:
            解析后的检查结果字典
        """
        lines = result_text.split("\n")
        result = {"符合要求": False, "具体问题": "", "改进建议": ""}

        for line in lines:
            line = line.strip()
            if line.startswith("符合要求："):
                value = line.split("符合要求：")[1].strip()
                result["符合要求"] = value == "是"
            elif line.startswith("具体问题："):
                result["具体问题"] = line.split("具体问题：")[1].strip()
            elif line.startswith("改进建议："):
                result["改进建议"] = line.split("改进建议：")[1].strip()

        return result
