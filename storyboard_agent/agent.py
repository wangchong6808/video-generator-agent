from agent_base.responses_agent import ResponsesAgent
from agent_base.tool_registry import ToolRegistry
from . import tool_definitions
from .storyboard_generator import StoryboardGeneratorTool
from .storyboard_scoring import StoryboardScoringTool
from volcenginesdkarkruntime import Ark
from loguru import logger
import sys
import os
import json
from typing import Dict

logger.remove()
logger.add(sink=sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <blue>{module}:{line}</blue> - {message}", level="DEBUG")


# 初始化并导出storyboard_agent对象
api_key = os.getenv("ARK_API_KEY")
if api_key:
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=api_key
    )
    storyboard_generator = StoryboardGeneratorTool(client)
    storyboard_scoring = StoryboardScoringTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(storyboard_generator.generate, tool_definitions.STORYBOARD_GENERATOR_TOOL)
    tool_registry.register_tool(storyboard_scoring.score, tool_definitions.STORYBOARD_SCORING_TOOL)
    
    storyboard_agent = ResponsesAgent(
        name="storyboard_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的分镜生成助手，擅长将剧本内容分解为多个合适的分镜。
            
        工作流程：
        1. 接收用户提供的剧本内容和关键元素
        2. 调用storyboard_generator工具，根据剧本内容和关键元素生成多个分镜，每个分镜对应5秒视频，包含相关的关键元素
        3. 调用storyboard_scoring工具，为生成的分镜打分
        4. 返回分镜列表和评分结果

        返回结果格式：
        {
            "storyboards": [
                {
                    "分镜编号": "1",
                    "镜头类型": "全景",
                    "首帧图片提示词": "提示词内容",
                    "视频生成提示词": "提示词内容",
                    "时长": 5,
                    "相关角色": ["角色1", "角色2"],
                    "相关道具": ["道具1", "道具2"],
                    "相关场景": ["场景1"]
                }
            ],
            "score": "83",
            "feedback": "分镜质量评估反馈"
        }
        """,
        description="根据剧本内容和关键元素生成多个分镜，每个分镜对应5秒视频，并对生成的分镜进行评分",
        tool_registry=tool_registry
    )


def generate_storyboard(script_content: str, key_elements: Dict = None) -> Dict:
    """
    根据剧本内容和关键元素生成分镜并评分
    
    Args:
        script_content: 剧本内容
        key_elements: 关键元素，包含角色、道具和场景，可选
        
    Returns:
        包含生成的分镜列表、评分和反馈的字典
    """
    logger.info("调用分镜生成智能体处理用户需求...")
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        raise ValueError("ARK_API_KEY must be provided either as parameter or environment variable")
        
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=api_key
    )
    storyboard_generator = StoryboardGeneratorTool(client)
    storyboard_scoring = StoryboardScoringTool(client)
    
    tool_registry = ToolRegistry()
    tool_registry.register_tool(storyboard_generator.generate, tool_definitions.STORYBOARD_GENERATOR_TOOL)
    tool_registry.register_tool(storyboard_scoring.score, tool_definitions.STORYBOARD_SCORING_TOOL)
    
    storyboard_agent = ResponsesAgent(
        name="storyboard_agent",
        model_name="doubao-seed-1-6-251015",
        instruction="""
        你是一个专业的分镜生成助手，擅长将剧本内容分解为多个合适的分镜。
            
        工作流程：
        1. 接收用户提供的剧本内容和关键元素
        2. 调用storyboard_generator工具，根据剧本内容和关键元素生成多个分镜，每个分镜对应5秒视频，包含相关的关键元素
        3. 调用storyboard_scoring工具，为生成的分镜打分
        4. 返回分镜列表和评分结果

        返回结果格式：
        {
            "storyboards": [
                {
                    "分镜编号": "1",
                    "镜头类型": "全景",
                    "首帧图片提示词": "提示词内容",
                    "视频生成提示词": "提示词内容",
                    "时长": 5,
                    "相关角色": ["角色1", "角色2"],
                    "相关道具": ["道具1", "道具2"],
                    "相关场景": ["场景1"]
                }
            ],
            "score": "83",
            "feedback": "分镜质量评估反馈"
        }
        """,
        description="根据剧本内容和关键元素生成多个分镜，每个分镜对应5秒视频，并对生成的分镜进行评分",
        tool_registry=tool_registry
    )
    
    # 构建用户输入，包含剧本内容和关键元素
    if key_elements:
        user_input = f"剧本内容：\n{script_content}\n\n关键元素：\n{json.dumps(key_elements, ensure_ascii=False, indent=2)}"
    else:
        user_input = script_content
    
    result = storyboard_agent.run(user_input)
    
    logger.info(f"分镜生成结果: {result}")
    return result


if __name__ == "__main__":
    # 示例剧本内容
    sample_script = """
    场景一、内景、客厅、白天

    【客厅光线柔和，陈设简朴。墙上的老式挂钟滴答作响，是室内唯一的声音。米白色沙发上，李华端坐着，手里攥着一封折痕明显的信纸，眉头紧锁，指尖无意识摩挲着纸边。】

    （敲门声突然响起，节奏平稳）

    李华
    （猛地回神，放下信纸起身，脚步略快地走向门口）

    【李华拉开木门，门外站着一位穿深色夹克的中年男人，背着黑色双肩包，面容温和。】

    王强
    （微微欠身）
    你好，我是王强，是你父亲的朋友。

    李华
    （眼神闪过一丝疑惑，随即侧身让路）
    请进吧。

    【王强走进客厅，李华关上门。两人在沙发对坐，王强将背包放在脚边。】

    王强
    （从背包里取出一个牛皮纸信封，递向李华）
    你父亲委托我，把这封信交给你。

    李华
    （接过信封，指节微白，迅速拆开。目光扫过信纸内容，脸色逐渐沉了下去，嘴唇抿成直线）

    李华
    我父亲他...

    【李华话音顿住，喉结滚动，看向王强。】

    王强
    （语气平静）
    他希望你能按照信里的指示去做。

    【李华沉默几秒，缓缓点头。】

    李华
    我会的。

    王强
    （露出浅淡的笑容，起身）
    很好。如果有不清楚的地方，随时联系我。

    【王强从口袋掏出一张名片，递给李华。】

    李华
    （接过名片，捏在掌心）
    谢谢。

    【李华送王强到门口，王强转身离开，门轻轻合上。】

    【李华回到沙发，重新坐下，将两封信（旧的和新的）平铺在膝头，再次拿起王强带来的那封。他的眼神从沉重转为坚定，拳头缓缓握紧。】

    李华
    （喃喃自语，声音低沉却有力）
    我一定会完成你的心愿的。

    【挂钟的滴答声再次清晰，李华的目光牢牢锁定在信纸上，一动不动。】
    """
    
    # 示例关键元素
    sample_key_elements = {
        "角色": [
            {
                "名称": "李华",
                "年龄": 30,
                "性别": "男",
                "体型": "中等身材",
                "眼睛颜色": "黑色",
                "发饰": "黑色短发",
                "衣着": "灰色休闲装",
                "鞋履": "白色运动鞋",
                "关键词": "主角、收到父亲的信、情绪变化"
            },
            {
                "名称": "王强",
                "年龄": 45,
                "性别": "男",
                "体型": "中等身材，略微发福",
                "眼睛颜色": "黑色",
                "发饰": "黑色短发，略带白发",
                "衣着": "深色夹克，黑色裤子",
                "鞋履": "黑色皮鞋",
                "关键词": "父亲的朋友、送信人、温和"
            }
        ],
        "道具": [
            {
                "名称": "信纸",
                "类别": "文书",
                "形状": "长方形，有折痕",
                "关键词": "父亲的信、重要线索"
            },
            {
                "名称": "挂钟",
                "类别": "家具",
                "形状": "圆形，老式",
                "关键词": "客厅装饰、时间流逝"
            },
            {
                "名称": "黑色双肩包",
                "类别": "箱包",
                "形状": "长方形，黑色",
                "关键词": "王强携带、装着信封"
            },
            {
                "名称": "牛皮纸信封",
                "类别": "文书",
                "形状": "长方形，牛皮纸色",
                "关键词": "父亲的信、王强带来"
            },
            {
                "名称": "名片",
                "类别": "文书",
                "形状": "长方形，白色",
                "关键词": "王强的联系方式"
            }
        ],
        "场景": [
            {
                "名称": "客厅",
                "类别": "室内场景",
                "关键词": "光线柔和、陈设简朴、挂钟滴答作响"
            },
            {
                "名称": "门口",
                "类别": "室内场景",
                "关键词": "木门、王强站在门外"
            }
        ]
    }
    
    # 调用分镜生成函数，传递剧本内容和关键元素
    generate_storyboard(sample_script, sample_key_elements)
