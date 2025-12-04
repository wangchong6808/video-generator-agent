from veadk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from .image_checker_tool import image_check
from .image_scoring import score

image_scoring_agent = Agent(
    name="image_scoring_agent",
    model_name="doubao-seed-1-6-251015",
    instruction="""
        你是一个专业的AI图片评估师，擅长基于给定的提示词对生成的图片结果进行评估并给出评分和具体问题。
        
        工作流程：
        1. 接收用户提供的提示词和图片URL
        2. 使用score工具调用doubao-seed-1-6-251015模型检查图片与提示词的符合程度
        3. 根据检查结果返回最终评估结果，包含评分和具体问题
   
        最终返回结果：
        直接返回score工具的返回结果
        """,
    description="图片评分智能体，根据输入的提示词和图片链接对图片结果进行评估并给出评分和具体问题",
    tools=[score],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)
