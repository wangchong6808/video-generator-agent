from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import os
import logging

# 导入各个智能体
from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
import video_agent.tool_definitions as tool_definitions
from .prompt_optimizer import VideoPromptOptimizer
from .video_generator import VideoGeneratorTool
from .video_scoring import VideoScoringTool
from volcenginesdkarkruntime import Ark
from loguru import logger
import sys

from typing import Dict


logger.remove()
logger.add(sink=sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <blue>{module}:{line}</blue> - {message}", level="INFO")

def generate_video(prompt: str, image_url: str = "") -> Dict:
# 初始化并导出video_agent对象
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        logger.error("ARK_API_KEY环境变量未设置")
        return {"error": "ARK_API_KEY环境变量未设置"}
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=api_key
    )
    prompt_optimizer = VideoPromptOptimizer(client)
    video_generator = VideoGeneratorTool(client)
    video_scoring = VideoScoringTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(prompt_optimizer.optimize, tool_definitions.VIDEO_PROMPT_OPTIMIZER_TOOL)
    tool_registry.register_tool(video_generator.generate, tool_definitions.VIDEO_GENERATOR_TOOL)
    tool_registry.register_tool(video_scoring.score, tool_definitions.VIDEO_SCORING_TOOL)
    
    video_agent = ResponsesAgent(
        name="video_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业视频生成助手，擅长协调多个智能体完成复杂的视频生成任务。你会对生成的视频做评分，确保视频符合要求。
        支持两种视频生成方式：
        - 文生视频：根据文本提示词生成视频
        - 首帧参考图生视频：根据文本提示词和首帧参考图生成视频
            
        工作流程：
        1. 接收用户的视频生成需求, 从用户需求中提取出生图提示词和其他参数，包括分辨率，视频时长，首帧图URL等
        2. 调用video_prompt_optimizer优化视频生成提示词，注意不要传入分辨率，视频时长，首帧图URL等其他参数
        3. 根据用户需求选择生成方式：
           - 如果用户提供了首帧参考图URL，调用video_generator并传递image_url参数
           - 否则，调用video_generator仅使用提示词
        4. 调用video_scoring为生成的视频打分
        5. 如果视频得分低于60分，重复步骤3-4，直到视频得分符合要求
        6. 如果视频得分符合要求，返回视频URL和评分

        返回结果格式：
        {
            "video_url": "https://example.com/generated_video.mp4",
            "score": "83"
        }
        """,
        description="根据视频生成需求生成高质量视频，支持文生视频和首帧参考图生视频两种方式，并返回生成的视频URL和评分",
        tool_registry=tool_registry
    )
    if image_url:
        prompt = prompt + "首帧图URL："+image_url
    result = video_agent.run(prompt)
    logger.info(f"生成视频结果: {result}")
    return result




if __name__ == "__main__":
    generate_video("生成两只兔子在草地上玩耍的视频，视频时长5秒，分辨率720P", "https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-0/021764817104005c2dd50d19df53a1cf97de1fb7620a49a868218_0.jpeg")
