from typing import Dict, List
from volcenginesdkarkruntime import Ark
from agent_base.utils import parse_response
from loguru import logger
import json


class StoryboardGeneratorTool:
    """分镜生成工具"""
    
    def __init__(self, client: Ark):
        """
        初始化分镜生成工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"
    
    def generate(self, script_content: str) -> Dict:
        """
        根据剧本内容生成多个分镜，每个分镜包含用于生成首帧图片的提示词和生成视频的提示词
        
        Args:
            script_content: 剧本内容
            
        Returns:
            包含生成的分镜列表的字典
        """
        storyboard_prompt_template = """
你是一个专业的分镜设计师，擅长将剧本内容分解为多个合适的分镜，上限不会超过5个分镜。

请根据以下剧本内容生成多个分镜，要求：
1. 自动判断合适的分镜数量，每个分镜对应5秒视频
2. 每个分镜包含：
   - 分镜编号
   - 镜头类型（如：全景、中景、近景、特写等）
   - 首帧图片提示词：用于生成该分镜的首帧图片
   - 视频生成提示词：用于生成该分镜的5秒视频
   - 时长：固定为5秒
3. 生成详细、精确的图片生成提示词，包含以下要素：
    - 主体内容
    - 场景描述
    - 风格要求
    - 细节描述
    - 光线和色彩
    - 构图要求
4. 请根据用户需求生成详细、精确的视频生成提示词，包含以下要素：
    - 主体内容
    - 场景描述
    - 风格要求
    - 动态效果
    - 光线和色彩
    - 动作描述
    - 场景变化

剧本内容：
{script_content}

请使用以下JSON格式返回分镜结果：
{{
    "storyboards": [
        {{
            "分镜编号": "1",
            "镜头类型": "全景",
            "首帧图片提示词": "提示词内容",
            "视频生成提示词": "提示词内容",
            "时长": 5
        }},
        {{
            "分镜编号": "2",
            "镜头类型": "中景",
            "首帧图片提示词": "提示词内容",
            "视频生成提示词": "提示词内容",
            "时长": 5
        }}
    ]
}}
        """
        
        prompt = storyboard_prompt_template.format(script_content=script_content)
        
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt
                        }
                    ]
                }
            ],
            store=True
        )
        
        # 提取分镜内容
        parsed_response = parse_response(response)
        storyboard_content = "".join(parsed_response["message"])
        
        logger.info(f"生成的分镜内容: {storyboard_content}")
        
        try:
            return json.loads(storyboard_content)
        except json.JSONDecodeError:
            # 如果返回格式不符合要求，返回空列表
            return {
                "storyboards": []
            }
