from typing import Dict, List

# 提示词优化工具定义
VIDEO_PROMPT_OPTIMIZER_TOOL: Dict = {
    "type": "function",
    "name": "video_prompt_optimizer",
    "description": "将用户的自然语言需求转换为高质量的视频生成提示词",
    "parameters": {
        "type": "object",
        "properties": {
            "user_input": {
                "type": "string",
                "description": "用户的原始视频生成需求"
            },
            "feedback": {
                "type": "string",
                "description": "视频检查反馈，用于迭代优化提示词",
                "default": ""
            }
        },
        "required": ["user_input"]
    }
}

# 视频生成工具定义
VIDEO_GENERATOR_TOOL: Dict = {
    "type": "function",
    "name": "video_generator",
    "description": "根据提示词生成视频",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "优化后的视频生成提示词"
            },
            "duration": {
                "type": "integer",
                "description": "视频时长（秒），默认5秒",
                "default": 5
            },
            "resolution": {
                "type": "string",
                "description": "视频分辨率，默认720P",
                "default": "720P"
            }
        },
        "required": ["prompt"]
    }
}

# 视频检查工具定义
VIDEO_SCORING_TOOL: Dict = {
    "type": "function",
    "name": "video_scoring",
    "description": "为生成的视频打分，评估其是否符合提示词要求",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "生成视频时使用的提示词"
            },
            "video_url": {
                "type": "string",
                "description": "生成的视频URL"
            }
        },
        "required": ["prompt", "video_url"]
    }
}

# 所有工具列表
ALL_TOOLS: List[Dict] = [
    VIDEO_PROMPT_OPTIMIZER_TOOL,
    VIDEO_GENERATOR_TOOL,
    VIDEO_SCORING_TOOL
]
