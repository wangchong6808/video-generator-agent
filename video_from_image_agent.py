from veadk import Runner, Agent
from veadk.memory.short_term_memory import ShortTermMemory
import asyncio
import logging

# 导入完整的image_agent和video_agent
from image_agent.agent import image_agent
from video_agent.agent import video_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

root_agent = Agent(
    name="video_from_image_agent",
    model_name="doubao-seed-1-6-251015",
    instruction="""
    你是一个专业视频生成助手，擅长协调多个智能体完成复杂的视频生成任务。你会先调用image_agent生成图片，然后基于生成的图片调用video_agent生成视频。
    
    可用的智能体：
    - image_agent：根据生图需求生成高质量图片，并返回生成的图片URL
    - video_agent：根据视频生成需求生成高质量视频，并返回生成的视频URL
    """,
    description="根据视频生成需求先生成图片，再基于图片生成视频，并返回视频URL",
    sub_agents=[image_agent, video_agent]
)

runner = Runner(agent=root_agent, short_term_memory=ShortTermMemory())



async def start():
    print("\n调用视频生成智能体处理用户需求...")
    response = await runner.run(
        messages="生成两只兔子在草地上玩耍的视频，视频时长5秒，分辨率720P", 
        session_id="video_from_image_session_123"
    )
    print(f"视频生成智能体结果：{response}")

if __name__ == "__main__":
    asyncio.run(start())
