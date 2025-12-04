from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
import script_agent.tool_definitions as tool_definitions
from .script_generator import ScriptGeneratorTool
from .script_scoring import ScriptScoringTool
from volcenginesdkarkruntime import Ark
from loguru import logger
import sys
import os
from typing import Dict

logger.remove()
logger.add(sink=sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <blue>{module}:{line}</blue> - {message}", level="DEBUG")


# 初始化并导出script_agent对象
api_key = os.getenv("ARK_API_KEY")
if api_key:
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=api_key
    )
    script_generator = ScriptGeneratorTool(client)
    script_scoring = ScriptScoringTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(script_generator.generate, tool_definitions.SCRIPT_GENERATOR_TOOL)
    tool_registry.register_tool(script_scoring.score, tool_definitions.SCRIPT_SCORING_TOOL)
    
    script_agent = ResponsesAgent(
        name="script_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的剧本生成助手，擅长将小说内容改编成符合传统剧本格式的剧本，并对生成的剧本进行评分。
            
        工作流程：
        1. 接收用户提供的小说内容
        2. 调用script_generator工具，根据小说内容生成符合传统剧本格式的剧本
        3. 调用script_scoring工具，为生成的剧本打分
        4. 返回剧本内容和评分结果

        返回结果格式：
        {
            "script_content": "生成的剧本内容",
            "score": "83",
            "feedback": "剧本质量评估反馈"
        }
        """,
        description="根据小说内容生成符合传统剧本格式的剧本，并对生成的剧本进行评分",
        tool_registry=tool_registry
    )


def generate_script(novel_content: str) -> Dict:
    """
    根据小说内容生成剧本并评分
    
    Args:
        novel_content: 小说内容
        
    Returns:
        包含生成的剧本内容、评分和反馈的字典
    """
    logger.info("调用剧本生成智能体处理用户需求...")
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        raise ValueError("ARK_API_KEY must be provided either as parameter or environment variable")
        
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=api_key
    )
    script_generator = ScriptGeneratorTool(client)
    script_scoring = ScriptScoringTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(script_generator.generate, tool_definitions.SCRIPT_GENERATOR_TOOL)
    tool_registry.register_tool(script_scoring.score, tool_definitions.SCRIPT_SCORING_TOOL)
    
    script_agent = ResponsesAgent(
        name="script_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的剧本生成助手，擅长将小说内容改编成符合传统剧本格式的剧本，并对生成的剧本进行评分。
            
        工作流程：
        1. 接收用户提供的小说内容
        2. 调用script_generator工具，根据小说内容生成符合传统剧本格式的剧本
        3. 调用script_scoring工具，为生成的剧本打分
        4. 返回剧本内容和评分结果

        返回结果格式：
        {
            "script_content": "生成的剧本内容",
            "score": "83",
            "feedback": "剧本质量评估反馈"
        }
        """,
        description="根据小说内容生成符合传统剧本格式的剧本，并对生成的剧本进行评分",
        tool_registry=tool_registry
    )
    
    result = script_agent.run(novel_content)
    logger.info(f"剧本生成结果: {result}")
    return result


if __name__ == "__main__":
    # 示例小说内容
    sample_novel = """
    房间里很安静，只有时钟滴答滴答的声音。李华坐在沙发上，手里拿着一封信，眉头紧锁。
    突然，敲门声响起，打断了他的思绪。他起身去开门，门外站着一个陌生人。
    "你好，我是王强，是你父亲的朋友。"陌生人说道。
    李华愣了一下，然后请他进来。两人在客厅里坐下，开始交谈。
    "你父亲委托我给你带一封信。"王强说着，从包里拿出一封信，递给李华。
    李华接过信，拆开来看。看完信后，他的脸色变得沉重。
    "我父亲他..."李华欲言又止。
    "他希望你能按照信里的指示去做。"王强说道。
    李华沉默了一会儿，然后点了点头。
    "我会的。"他说道。
    "很好。"王强笑了笑，然后站起身来。
    "我该走了，如果你有什么问题，可以随时联系我。"他说着，递给李华一张名片。
    李华接过名片，然后送王强出门。
    门关上后，李华回到沙发上，再次打开那封信。他的眼神变得坚定起来。
    "我一定会完成你的心愿的。"他喃喃自语道。
    """
    
    # 调用剧本生成函数
    generate_script(sample_novel)
