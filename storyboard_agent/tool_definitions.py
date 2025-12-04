from typing import Dict, List

# 分镜生成工具定义
STORYBOARD_GENERATOR_TOOL: Dict = {
    "type": "function",
    "name": "storyboard_generator",
    "description": "根据剧本内容生成多个分镜，每个分镜包含用于生成首帧图片的提示词和生成视频的提示词",
    "parameters": {
        "type": "object",
        "properties": {
            "script_content": {
                "type": "string",
                "description": "剧本内容，用于生成分镜"
            }
        },
        "required": ["script_content"]
    }
}

# 分镜打分工具定义
STORYBOARD_SCORING_TOOL: Dict = {
    "type": "function",
    "name": "storyboard_scoring",
    "description": "为生成的分镜打分，评估其质量和可用性",
    "parameters": {
        "type": "object",
        "properties": {
            "storyboard_content": {
                "type": "string",
                "description": "生成的分镜内容"
            }
        },
        "required": ["storyboard_content"]
    }
}

# 所有工具列表
ALL_TOOLS: List[Dict] = [
    STORYBOARD_GENERATOR_TOOL,
    STORYBOARD_SCORING_TOOL
]
