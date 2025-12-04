import logging
import json
import os
from typing import Dict

# 导入必要的类和函数
from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
from image_agent.agent import generate_image as generate_image_func
from video_agent.agent import generate_video as generate_video_func

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 工具定义
GENERATE_IMAGE_TOOL = {
    "type": "function",
    "name": "generate_image",
    "description": "根据提示词生成图片",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "图片生成提示词"
            }
        },
        "required": ["prompt"]
    }
}

GENERATE_VIDEO_TOOL = {
    "type": "function",
    "name": "generate_video",
    "description": "根据提示词和首帧参考图生成视频",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "视频生成提示词"
            },
            "image_url": {
                "type": "string",
                "description": "首帧参考图URL"
            }
        },
        "required": ["prompt", "image_url"]
    }
}


# 包装函数，使其能作为工具使用
def generate_image_tool(prompt: str) -> Dict:
    """
    图片生成工具包装函数
    """
    result = generate_image_func(prompt)
    return result


def generate_video_tool(prompt: str, image_url: str) -> Dict:
    """
    视频生成工具包装函数
    """
    result = generate_video_func(prompt, image_url)
    return result


# 主函数
def main(user_input):
    """
    主函数，演示使用Responses API实现生图和生视频的连续逻辑
    """
    logger.info("初始化从图片生成视频的智能体...")
    
    # 创建工具注册表
    tool_registry = ToolRegistry()
    
    # 注册工具
    tool_registry.register_tool(generate_image_tool, GENERATE_IMAGE_TOOL)
    tool_registry.register_tool(generate_video_tool, GENERATE_VIDEO_TOOL)
    
    # 创建ResponsesAgent实例
    video_from_image_agent = ResponsesAgent(
        name="video_from_image_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的视频生成助手，擅长协调多个工具完成从图片生成视频的任务。
        
        工作流程：
        1. 接收用户的视频生成需求
        2. 首先调用generate_image工具，根据提示词生成图片
        3. 从图片生成结果中提取图片URL
        4. 然后调用generate_video工具，使用生成的图片作为首帧参考图生成视频
        5. 从视频生成结果中提取视频URL和评分
        6. 最终返回包含图片URL、视频URL和评分的JSON结果
        
        返回结果格式：
        {
            "image_url": "生成的图片URL",
            "video_url": "生成的视频URL",
            "score": "视频评分"
        }
        """,
        description="根据视频生成需求先生成图片，再基于图片生成视频，并返回视频URL和评分",
        tool_registry=tool_registry
    )
    
    # 运行智能体
    logger.info(f"向智能体发送请求：{user_input}")
    
    result = video_from_image_agent.run(user_input)
    
    logger.info(f"智能体执行结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
    return result


if __name__ == "__main__":
    # 示例调用
    main("生成两只兔子在草地上玩耍的视频，写实风格，视频时长5秒，分辨率720P")

