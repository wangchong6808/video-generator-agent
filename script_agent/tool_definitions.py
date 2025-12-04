from typing import Dict, List

# 剧本生成工具定义
SCRIPT_GENERATOR_TOOL: Dict = {
    "type": "function",
    "name": "script_generator",
    "description": "根据小说内容生成符合传统剧本格式的剧本",
    "parameters": {
        "type": "object",
        "properties": {
            "novel_content": {
                "type": "string",
                "description": "小说内容，用于生成剧本"
            }
        },
        "required": ["novel_content"]
    }
}

# 剧本打分工具定义
SCRIPT_SCORING_TOOL: Dict = {
    "type": "function",
    "name": "script_scoring",
    "description": "为生成的剧本打分，评估其是否符合传统剧本格式和质量要求",
    "parameters": {
        "type": "object",
        "properties": {
            "script_content": {
                "type": "string",
                "description": "生成的剧本内容"
            }
        },
        "required": ["script_content"]
    }
}

# 关键元素提取工具定义
SCRIPT_KEY_ELEMENTS_EXTRACTOR_TOOL: Dict = {
    "type": "function",
    "name": "script_key_elements_extractor",
    "description": "从剧本内容中提取关键元素，包括角色、道具和场景",
    "parameters": {
        "type": "object",
        "properties": {
            "script_content": {
                "type": "string",
                "description": "剧本内容，用于提取关键元素"
            }
        },
        "required": ["script_content"]
    }
}

# 所有工具列表
ALL_TOOLS: List[Dict] = [
    SCRIPT_GENERATOR_TOOL,
    SCRIPT_SCORING_TOOL,
    SCRIPT_KEY_ELEMENTS_EXTRACTOR_TOOL
]
