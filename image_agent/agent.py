from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import os
import logging

# 导入各个智能体
from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
import image_agent.tool_definitions as tool_definitions
from .prompt_optimizer import PromptOptimizer
from .image_generator import ImageGeneratorTool
from .image_scoring import ImageScoringTool
from volcenginesdkarkruntime import Ark
from loguru import logger
import sys

logger.remove()
logger.add(sink=sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <blue>{module}:{line}</blue> - {message}", level="INFO")



from typing import Dict

def generate_image(prompt: str) -> Dict:
    logger.info("调用编排智能体处理用户需求...")
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        raise ValueError("ARK_API_KEY must be provided either as parameter or environment variable")
        
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=api_key
    )
    prompt_optimizer = PromptOptimizer(client)
    image_generator = ImageGeneratorTool(client)
    image_scoring = ImageScoringTool(client)
    
    tool_registry = ToolRegistry()
    # tool_registry.register_tool(prompt_optimizer.optimize, tool_definitions.PROMPT_OPTIMIZER_TOOL)
    tool_registry.register_tool(image_generator.generate, tool_definitions.IMAGE_GENERATOR_TOOL)
    tool_registry.register_tool(image_scoring.score, tool_definitions.IMAGE_SCORING_TOOL)
    image_agent = ResponsesAgent(
        name="image_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业图片生成助手，擅长协调多个智能体完成复杂的图片生成任务。你会对生成的图片做评分，确保图片符合要求。
            
        工作流程：
        1. 接收用户的图片生成需求
        2. 调用prompt_agent优化图片生成提示词
        3. 调用image_generator_agent根据提示词生成图片，获取图片URL
        4. 调用image_scoring_agent为生成的图片打分, 以markdown格式返回评分和图片URL
        5. 如果图片图片得分低于60分，重复步骤3-4，直到图片得分符合要求
        6. 如果图片得分符合要求，返回图片URL和评分

        返回结果格式：
        {
            "image_url": "https://example.com/generated_image.jpg",
            "score": "83"
        }
        """,
        description="根据生图需求生成高质量图片，并返回生成的图片URL和评分",
        tool_registry=tool_registry
    )
    result = image_agent.run(prompt)
    logger.info(f"生成图片结果: {result}")
    return result

if __name__ == "__main__":
    generate_image("生成一张关于城市交通的图片")

