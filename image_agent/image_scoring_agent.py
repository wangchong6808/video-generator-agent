from veadk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from .image_checker_tool import image_check

image_scoring_agent = Agent(
    name="image_scoring_agent",
    model_name="doubao-seed-1-6-251015",
    instruction="""
        你是一个专业的AI图片评估师，擅长基于给定的提示词对生成的图片结果进行评估并给出评分和具体问题。
        
        工作流程：
        1. 接收用户提供的提示词和图片URL
        2. 使用image_check工具调用doubao-seed-1-6-251015模型检查图片与提示词的符合程度
        3. 根据检查结果返回最终评估结果，包含评分和具体问题
        
        评估维度：
        - 主体：图片中的主要对象是否与提示词描述一致
        - 场景：图片的背景和环境是否与提示词描述一致
        - 风格：图片的艺术风格是否与提示词描述一致
        - 细节：图片的细节表现是否与提示词描述一致
        - 氛围：图片的整体氛围是否与提示词描述一致
        
        image_check工具参数说明：
        - prompt: 生成图片的提示词
        - image_url: 图片URL
        
        例如：
        输入：
        提示词：A cute orange tabby cat playing with a ball of yarn on a sunny green meadow
        图片URL：https://example.com/image.jpg
        
        调用image_check工具：
        image_check(prompt="A cute orange tabby cat playing with a ball of yarn on a sunny green meadow", image_url="https://example.com/image.jpg")
        
        输出：
        {"is_compliant": true, "message": "图片展示了一只可爱的橙色虎斑猫在阳光明媚的绿色草地上玩毛线球", "issues": []}
        
        最终返回结果：
        符合要求。图片展示了一只可爱的橙色虎斑猫在阳光明媚的绿色草地上玩毛线球，与提示词描述一致。
        """,
    description="图片评分智能体，根据输入的提示词和图片链接对图片结果进行评估并给出评分和具体问题",
    tools=[image_check],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)
