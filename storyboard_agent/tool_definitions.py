from typing import Dict, List

# 分镜生成工具定义
STORYBOARD_GENERATOR_TOOL: Dict = {
    "type": "function",
    "name": "storyboard_generator",
    "description": "根据剧本内容和关键元素生成多个分镜，每个分镜包含用于生成首帧图片的提示词、生成视频的提示词以及相关的关键元素",
    "parameters": {
        "type": "object",
        "properties": {
            "script_content": {
                "type": "string",
                "description": "剧本内容，用于生成分镜"
            },
            "key_elements": {
                "type": "object",
                "description": "关键元素，包含角色、道具和场景",
                "properties": {
                    "角色": {
                        "type": "array",
                        "description": "角色列表"
                    },
                    "道具": {
                        "type": "array",
                        "description": "道具列表"
                    },
                    "场景": {
                        "type": "array",
                        "description": "场景列表"
                    }
                }
            }
        },
        "required": ["script_content", "key_elements"]
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
