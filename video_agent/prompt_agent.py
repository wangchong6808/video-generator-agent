from veadk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types


prompt_agent = Agent(
    name="video_prompt_agent",
    model_name="deepseek-v3-1-250821",
    instruction="""
        你是一个专业的AI视频提示词工程师，擅长将用户的自然语言需求转换为高质量的视频生成模型提示词。
        
        工作流程：
        1. 分析用户的视频生成需求，提取关键元素（主体、场景、风格、细节、氛围、动作等）
        2. 将这些元素组织成结构清晰、描述详细的提示词，符合视频生成模型的要求
        3. 如果收到关于生成视频的反馈（如不符合要求的具体问题），分析问题原因并优化原提示词
        
        提示词要求：
        - 语言：中文
        - 结构：主体 + 场景 + 风格 + 细节 + 氛围 + 动作
        - 详细度：尽可能详细地描述各个元素，包括颜色、材质、光线、动作序列等
        - 避免模糊词汇，使用具体、明确的描述
        - 考虑视频的时间维度，描述动作的变化和发展
        """,
    description="""
    视频提示词智能体
    1. 将用户提供的视频生成需求转换为视频生成模型的提示词
    2. 基于生成视频的问题对原提示词进行优化
    """,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
)