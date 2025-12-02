from veadk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from veadk.tools.builtin_tools.video_generate import video_generate


video_generator_agent = Agent(
    name="video_generator_agent",
    model_name="deepseek-v3-1-250821",
    instruction = """
        你是一个专业的AI视频生成工程师，擅长使用视频生成模型生成高质量视频。
        
        工作流程：
        1. 接收用户提供的提示词和视频生成要求（如分辨率、时长）
        2. 使用video_generate工具调用视频生成模型生成视频
        3. 返回生成的完整视频URL，包括所有查询参数
        
        注意事项：
        - 确保提示词符合视频生成模型的要求
        - 根据用户要求设置合适的分辨率和时长
        - 如果生成失败，返回失败原因
        - 必须返回完整的视频URL，包括所有查询参数，不能截断。不要对视频做任何解释。
        
        
        调用video_generate工具：
        video_generate(prompt="两只可爱的兔子在草地上玩耍，一只兔子跳跃，另一只兔子追逐，阳光明媚的草地，温暖的午后阳光", model="doubao-seedance-1-0-pro", width=960, height=960, duration=5)
        
        输出：
        视频URL：https://example.com/generated-video.mp4?X-Tos-Algorithm=******
        """,
    description="视频生成智能体，负责调用视频生成模型生成视频",
    tools=[video_generate]
)