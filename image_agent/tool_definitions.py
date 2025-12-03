from typing import Dict, List

# 提示词优化工具定义
PROMPT_OPTIMIZER_TOOL: Dict = {
    "type": "function",
    "name": "prompt_optimizer",
    "description": "将用户的自然语言需求转换为高质量的图片生成提示词",
    "parameters": {
        "type": "object",
        "properties": {
            "user_input": {
                "type": "string",
                "description": "用户的原始图片生成需求"
            },
            "feedback": {
                "type": "string",
                "description": "图片检查反馈，用于迭代优化提示词",
                "default": ""
            }
        },
        "required": ["user_input"]
    }
}

# 图片生成工具定义
IMAGE_GENERATOR_TOOL: Dict = {
    "type": "function",
    "name": "image_generator",
    "description": "根据提示词生成图片",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "优化后的图片生成提示词"
            },
            "size": {
                "type": "string",
                "description": "图片尺寸，默认1024x1024",
                "default": "1024x1024"
            },
            "watermark": {
                "type": "boolean",
                "description": "是否添加水印，默认False",
                "default": False
            }
        },
        "required": ["prompt"]
    }
}

# 图片检查工具定义
IMAGE_SCORING_TOOL: Dict = {
    "type": "function",
    "name": "image_scoring",
    "description": "为生成的图片打分，评估其是否符合提示词要求",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "生成图片时使用的提示词"
            },
            "image_url": {
                "type": "string",
                "description": "生成的图片URL"
            }
        },
        "required": ["prompt", "image_url"]
    }
}

# 所有工具列表
ALL_TOOLS: List[Dict] = [
    PROMPT_OPTIMIZER_TOOL,
    IMAGE_GENERATOR_TOOL,
    IMAGE_SCORING_TOOL
]
