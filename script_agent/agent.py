from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
import script_agent.tool_definitions as tool_definitions
from .script_generator import ScriptGeneratorTool
from .script_scoring import ScriptScoringTool
from .script_key_elements_extractor import ScriptKeyElementsExtractorTool
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
    script_key_elements_extractor = ScriptKeyElementsExtractorTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(script_generator.generate, tool_definitions.SCRIPT_GENERATOR_TOOL)
    tool_registry.register_tool(script_scoring.score, tool_definitions.SCRIPT_SCORING_TOOL)
    tool_registry.register_tool(script_key_elements_extractor.extract, tool_definitions.SCRIPT_KEY_ELEMENTS_EXTRACTOR_TOOL)
    
    script_agent = ResponsesAgent(
        name="script_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的剧本生成助手，擅长将小说内容改编成符合传统剧本格式的剧本，并对生成的剧本进行评分，同时提取关键元素。
            
        工作流程：
        1. 接收用户提供的小说内容
        2. 调用script_generator工具，根据小说内容生成符合传统剧本格式的剧本
        3. 调用script_scoring工具，为生成的剧本打分，如果剧本质量低于60分，重新执行第2步，否则继续执行第4步
        4. 将第2步生成的剧本作为输入，调用script_key_elements_extractor工具，从生成的剧本中提取关键元素，包括角色、道具和场景
        5. 返回剧本内容、评分结果和关键元素

        返回结果格式：
        {
            "script_content": "生成的剧本内容",
            "score": "83",
            "feedback": "剧本质量评估反馈",
            "key_elements": {
                "角色": [
                    {
                        "名称": "角色名",
                        "年龄": 数值,
                        "性别": "男/女",
                        "体型": "描述",
                        "眼睛颜色": "描述",
                        "发饰": "描述",
                        "衣着": "描述",
                        "鞋履": "描述",
                        "关键词": "关键词1、关键词2"
                    }
                ],
                "道具": [
                    {
                        "名称": "道具名",
                        "类别": "类别",
                        "形状": "描述",
                        "关键词": "关键词1、关键词2"
                    }
                ],
                "场景": [
                    {
                        "名称": "场景名",
                        "类别": "类别",
                        "关键词": "关键词1、关键词2"
                    }
                ]
            }
        }
        """,
        description="根据小说内容生成符合传统剧本格式的剧本，并对生成的剧本进行评分，同时提取关键元素",
        tool_registry=tool_registry
    )


def generate_script(novel_content: str) -> Dict:
    """
    根据小说内容生成剧本并评分，同时提取关键元素
    
    Args:
        novel_content: 小说内容
        
    Returns:
        包含生成的剧本内容、评分、反馈和关键元素的字典
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
    script_key_elements_extractor = ScriptKeyElementsExtractorTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(script_generator.generate, tool_definitions.SCRIPT_GENERATOR_TOOL)
    tool_registry.register_tool(script_scoring.score, tool_definitions.SCRIPT_SCORING_TOOL)
    tool_registry.register_tool(script_key_elements_extractor.extract, tool_definitions.SCRIPT_KEY_ELEMENTS_EXTRACTOR_TOOL)
    
    script_agent = ResponsesAgent(
        name="script_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的剧本生成助手，擅长将小说内容改编成符合传统剧本格式的剧本，并对生成的剧本进行评分，同时提取关键元素。
            
        工作流程：
        1. 接收用户提供的小说内容
        2. 调用script_generator工具，根据小说内容生成符合传统剧本格式的剧本
        3. 调用script_scoring工具，为生成的剧本打分
        4. 调用script_key_elements_extractor工具，从生成的剧本中提取关键元素，包括角色、道具和场景
        5. 返回剧本内容、评分结果和关键元素

        返回结果格式：
        {
            "script_content": "生成的剧本内容",
            "score": "83",
            "feedback": "剧本质量评估反馈",
            "key_elements": {
                "角色": [
                    {
                        "名称": "角色名",
                        "年龄": 数值,
                        "性别": "男/女",
                        "体型": "描述",
                        "眼睛颜色": "描述",
                        "发饰": "描述",
                        "衣着": "描述",
                        "鞋履": "描述",
                        "关键词": "关键词1、关键词2"
                    }
                ],
                "道具": [
                    {
                        "名称": "道具名",
                        "类别": "类别",
                        "形状": "描述",
                        "关键词": "关键词1、关键词2"
                    }
                ],
                "场景": [
                    {
                        "名称": "场景名",
                        "类别": "类别",
                        "关键词": "关键词1、关键词2"
                    }
                ]
            }
        }
        """,
        description="根据小说内容生成符合传统剧本格式的剧本，并对生成的剧本进行评分，同时提取关键元素",
        tool_registry=tool_registry
    )
    
    result = script_agent.run(novel_content)
    logger.info(f"剧本生成结果: {result}")
    return result


if __name__ == "__main__":
    # 示例小说内容
    sample_novel = """
    宇文化及卓立战舰指挥台之上，极目运河两岸。
    此时天尚未亮，在五艘巨舰的灯炷映照下，天上星月黯然失色，似在显示他宇文阀的兴起，使南方士族亦失去往日的光辉。
    宇文化及年在三十许间，身形高瘦，手足颀长，脸容古挫，神色冷漠，一对眼神深邃莫测，予人狠冷无情的印象，但亦另有一股震慑人心的霸气。
    这五艘战船乃已作古的隋朝开国的大臣杨素亲自督建，名为五牙大舰，甲板上楼起五层，高达十二丈，每舰可容战士八百之众。
    五桅布帆张满下，舰群以快似奔马的速度，朝运河下游江都开去。
    宇文化及目光落在岸旁林木外冒起的殿顶，那是隋炀帝杨广年前才沿河建成的四十多所行宫之一。
    隋炀帝杨广即位后，以北统南，命人开凿运河，贯通南北交通，无论在军事上或经济上，均有实际的需要。但大兴土木，营造行宫，又沿河遍植杨柳，就是劳民伤财之事了。
    站在他后侧的心腹手下张士和恭敬地道：“天亮前可抵江都，总管今趟倘能把《长生诀》取得再献给皇上，当是大功一件。”
    宇文化及嘴角逸出一丝高深莫测的笑意，淡淡道：“圣上醉心道家炼丹的长生不死之术，实在教人可哂，若真有此异术，早该有长生不死之人，可是纵观道家先贤，谁不是难逃一死。若非此书是以玄金线织成，水火不侵，我们只要随便找人假做一本，便可瞒混过去了。”
    张士和陪笑道：“圣上明察暗访十多年，始知此书落在被誉为扬州第一高手的“推山手”石龙手上，可笑那石龙奢望得书而不死，却偏因此书而亡，实在讽刺之极。”
    宇文化及冷哼一声，低声念了‘石龙’的名字。
    身上的血液立时沸腾起来。
    这些年来，由于位高权重，他已罕有与人交手了。
    现在机会终于来到。
    """
    
    # 调用剧本生成函数
    generate_script(sample_novel)
