from typing import Dict
from volcenginesdkarkruntime import Ark
from image_agent.utils import parse_response
from loguru import logger
import json
import os



def score(prompt: str, image_url: str) -> Dict:
    """
    基于提示词对生成的图片进行评分

    Args:
        prompt: 图片生成提示词
        image_url: 生成的图片URL

    Returns:
        {
            "评分": int, // 整数 0-100之间，例如 80
            "具体问题": str, // 分数低于60需要有此项内容
            "改进建议": str // 分数低于60需要有此项内容
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
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=os.getenv('VOLC_APIKEY', ''),
    )
    response = client.responses.create(
        model="doubao-seed-1-6-251015",
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


