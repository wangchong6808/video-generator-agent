from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import asyncio
import logging

# 导入各个智能体
from .prompt_agent import prompt_agent
from .image_generator_agent import image_generator_agent
from .image_checker_agent import image_checker_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


image_agent = Agent(
    name="image_agent",
    model_name="doubao-seed-1-6-251015",
    instruction="""
    你是一个专业生图助手，擅长协调多个智能体完成复杂的生图任务。你会对生成的图片做检查，确保图片符合要求。
        
    可用的智能体：
    - prompt_agent：将用户需求转换为生图模型的提示词，或者当生成的图片不符合要求时对提示词进行优化
    - image_generator_agent：根据提示词生成图片，但返回的图片质量可能不符合要求
    - image_checker_agent：检查生成的图片是否符合提示词要求
    """,
    description="根据生图需求生成高质量图片，并返回生成的图片URL",
    sub_agents=[prompt_agent, image_generator_agent, image_checker_agent]
)

# root_agent = orchestrator_agent

runner = Runner(
    agent=image_agent,
    short_term_memory=ShortTermMemory()
)

async def main():
    print("\n调用编排智能体处理用户需求...")
    response = await runner.run(
        messages="生成两只兔子在草地上玩耍的图片，分辨率为1024x1024", session_id="session_id123"
    )
    print(f"编排智能体结果：{response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

