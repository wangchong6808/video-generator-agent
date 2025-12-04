from typing import Dict
from volcenginesdkarkruntime import Ark
from agent_base.utils import parse_response
from loguru import logger
import json


class ScriptKeyElementsExtractorTool:
    """剧本关键元素提取工具"""
    
    def __init__(self, client: Ark):
        """
        初始化剧本关键元素提取工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"
    
    def extract(self, script_content: str) -> Dict:
        """
        从剧本内容中提取关键元素，包括角色、道具和场景
        
        Args:
            script_content: 剧本内容
            
        Returns:
            包含提取的关键元素（角色、道具和场景）的字典
        """
        key_elements_prompt_template = """
你是一个专业的剧本分析专家，擅长从剧本内容中提取关键元素。

请根据以下剧本内容提取关键元素，包括角色、道具和场景，要求：
1. 角色：包括名称、年龄、性别、体型、眼睛颜色、发饰、衣着、鞋履、关键词等信息
2. 道具：包括名称、类别、形状、关键词等信息
3. 场景：包括名称、类别、关键词等信息

剧本内容：
{script_content}

请使用以下JSON格式返回提取结果：
{{
    "角色": [
        {{
            "名称": "角色名",
            "年龄": 数值,
            "性别": "男/女",
            "体型": "描述",
            "眼睛颜色": "描述",
            "发饰": "描述",
            "衣着": "描述",
            "鞋履": "描述",
            "关键词": "关键词1、关键词2"
        }}
    ],
    "道具": [
        {{
            "名称": "道具名",
            "类别": "类别",
            "形状": "描述",
            "关键词": "关键词1、关键词2"
        }}
    ],
    "场景": [
        {{
            "名称": "场景名",
            "类别": "类别",
            "关键词": "关键词1、关键词2"
        }}
    ]
}}
        """
        
        prompt = key_elements_prompt_template.format(script_content=script_content)
        
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
        
        # 提取关键元素
        parsed_response = parse_response(response)
        key_elements_content = "".join(parsed_response["message"])
        
        logger.info(f"提取的关键元素: {key_elements_content}")
        
        try:
            return json.loads(key_elements_content)
        except json.JSONDecodeError:
            # 如果返回格式不符合要求，返回空结果
            return {
                "角色": [],
                "道具": [],
                "场景": []
            }
