from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import asyncio
import logging

# 导入各个智能体
from .prompt_agent import prompt_agent
from .video_generator_agent import video_generator_agent
from .video_checker_agent import video_checker_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


video_agent = Agent(
    name="video_agent",
    model_name="doubao-seed-1-6-251015",
    instruction="""
    你是一个专业视频生成助手，擅长协调多个智能体完成复杂的视频生成任务。你会对生成的视频做检查，确保视频符合要求。
    
    可用的智能体：
    - video_prompt_agent：将用户需求转换为视频生成模型的提示词，或者当生成的视频不符合要求时对提示词进行优化
    - video_generator_agent：根据提示词生成视频，但返回的视频质量可能不符合要求
    - video_checker_agent：检查生成的视频是否符合提示词要求
    
    工作流程：
    1. 接收用户的视频生成需求，包括可能的首帧图片URL（如果用户提供）
    2. 调用video_prompt_agent生成视频提示词
    3. 调用video_generator_agent根据提示词生成视频，获取视频URL
    4. 调用video_checker_agent检查生成的视频是否符合要求
    5. 如果视频符合要求，直接返回video_generator_agent生成的视频URL给用户
    
    注意事项：
    - 必须直接返回video_generator_agent生成的视频URL，包括所有查询参数，不能截断
    - 不要返回任何描述性文字，只返回视频URL
    - 不要添加任何前缀或后缀，只返回纯视频URL
    """,
    description="根据视频生成需求生成高质量视频，并返回生成的视频URL。如果用户提供首帧图片URL，视频生成模型会基于该图片进行生成。",
    sub_agents=[prompt_agent, video_generator_agent, video_checker_agent]
)

runner = Runner(
    agent=video_agent,
    short_term_memory=ShortTermMemory()
)

async def main():
    print("\n调用编排智能体处理用户需求...")
    response = await runner.run(
        messages="生成两只兔子在草地上玩耍的视频，分辨率480P，时长5秒", session_id="video_session_123"
    )
    print(f"编排智能体结果：{response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())