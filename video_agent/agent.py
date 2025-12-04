from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import os
import logging

# 导入各个智能体
from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
import tool_definitions
from prompt_optimizer import VideoPromptOptimizer
from video_generator import VideoGeneratorTool
from video_scoring import VideoScoringTool
from volcenginesdkarkruntime import Ark
from loguru import logger
import sys

logger.remove()
logger.add(sink=sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <blue>{module}:{line}</blue> - {message}", level="DEBUG")

# 初始化并导出video_agent对象
api_key = os.getenv("ARK_API_KEY")
if api_key:
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
            
        工作流程：
        1. 接收用户的视频生成需求
        2. 调用video_prompt_optimizer优化视频生成提示词
        3. 调用video_generator根据提示词生成视频，获取视频URL
        4. 调用video_scoring为生成的视频打分, 以markdown格式返回评分和视频URL
        5. 如果视频得分低于60分，重复步骤3-4，直到视频得分符合要求
        6. 如果视频得分符合要求，返回视频URL和评分

        返回结果格式：
        {
            "video_url": "https://example.com/generated_video.mp4",
            "score": "83"
        }
        """,
        description="根据视频生成需求生成高质量视频，并返回生成的视频URL和评分",
        tool_registry=tool_registry
    )

def main():
    logger.info("调用视频生成智能体处理用户需求...")
    if not api_key:
        raise ValueError("ARK_API_KEY must be provided either as parameter or environment variable")
    
    video_agent.run("生成两只兔子在草地上玩耍的视频，视频时长5秒，分辨率720P")


if __name__ == "__main__":
    main()
