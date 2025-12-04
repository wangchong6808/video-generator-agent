from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import asyncio
import logging

# 导入各个智能体
from .prompt_agent import prompt_agent
from .image_generator_agent import image_generator_agent
from .image_checker_agent import image_checker_agent
from .image_scoring_agent import image_scoring_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


image_agent = Agent(
    name="image_agent",
    model_name="doubao-seed-1-6-251015",
    instruction="""
    你是一个专业图片生成助手，擅长协调多个智能体完成复杂的图片生成任务。你会对生成的图片做评分，确保图片符合要求。
        
    工作流程：
    1. 接收用户的图片生成需求
    2. 调用prompt_agent优化图片生成提示词
    3. 调用image_generator_agent根据提示词生成图片，获取图片URL
    4. 调用image_scoring_agent为生成的图片打分, 获得评分和具体问题
    5. 如果image_scoring_agent的评分低于60分，重复步骤3和4，直到获得符合要求的图片
    6. 如果image_scoring_agent的评分高于等于60分，返回图片URL和评分

    返回结果格式：
    {
        "image_url": "https://example.com/generated_image.jpg",
        "score": 80
    }
    """,
    description="根据生图需求生成高质量图片，并返回生成的图片URL和评分",
    sub_agents=[prompt_agent, image_generator_agent, image_scoring_agent]
)

# root_agent = orchestrator_agent

runner = Runner(
    agent=image_agent,
    short_term_memory=ShortTermMemory()
)

async def main():
    print("\n调用编排智能体处理用户需求...")
    response = await runner.run(
        messages="生成两只兔子在草地上玩耍的图片，分辨率为1024x1024，需要图片URL和评分", session_id="session_id123"
    )
    print(f"编排智能体结果：{response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

