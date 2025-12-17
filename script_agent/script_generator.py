from typing import Dict
from volcenginesdkarkruntime import Ark
from agent_base.utils import parse_response
from loguru import logger
import json


class ScriptGeneratorTool:
    """剧本生成工具"""
    
    def __init__(self, client: Ark):
        """
        初始化剧本生成工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seed-1-6-251015"
    
    def generate(self, novel_content: str) -> Dict:
        """
        根据小说内容生成符合传统剧本格式的剧本
        
        Args:
            novel_content: 小说内容
            
        Returns:
            包含生成的剧本内容的字典
        """
        script_prompt_template = """
你是一个专业的编剧，擅长将小说内容改编成符合传统剧本格式的剧本。

请根据以下小说内容生成一个结构完整、格式规范的传统剧本：

{novel_content}

传统剧本格式要求：
1. 包含场景标题（如：场景一、内景、客厅、白天）
2. 包含角色名称和对话
3. 包含动作描述（用括号括起来）
4. 包含场景描述
5. 结构清晰，符合剧本写作规范
6. 保留原小说的核心情节和人物关系

请直接返回剧本内容，不要添加任何额外说明。
        """
        
        prompt = script_prompt_template.format(novel_content=novel_content)
        
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
        
        # 提取剧本内容
        parsed_response = parse_response(response)
        script_content = "".join(parsed_response["message"])
        
        logger.debug(f"生成的剧本内容: {script_content}")
        
        return {
            "script_content": script_content
        }
