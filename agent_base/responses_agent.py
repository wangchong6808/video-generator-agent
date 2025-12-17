import os
from volcenginesdkarkruntime import Ark
from typing import Dict
import agent_base.utils as utils
from loguru import logger
from agent_base.tool_registry import ToolRegistry
import json

class ResponsesAgent():
    def __init__(self, name, model_name, instruction, description, tool_registry: ToolRegistry, sub_agents=[]):
        self.name = name
        self.model_name = model_name
        self.instruction = instruction
        self.description = description
        self.tool_registry = tool_registry
        self.api_key = os.getenv("ARK_API_KEY")
        if not self.api_key:
            raise ValueError("ARK_API_KEY must be provided either as parameter or environment variable")
        
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=self.api_key
        )

    def run(self, user_input: str) -> Dict:
        """
        运行智能体，处理用户的图片生成需求
        
        Args:
            user_input: 用户的图片生成需求
            
        Returns:
            包含最终生成图片和相关信息的字典
        """
        # 构建初始对话历史 - 符合API文档的input结构
        # 注意：根据API文档，input是一个数组，包含不同类型的输入项
        input_messages = [
            # 系统提示词
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": self.instruction
                    }
                ]
            },
            # 用户输入
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_input
                    }
                ]
            }
        ]

        initial_response = self.client.responses.create(
            model=self.model_name,
            input=input_messages,
            tools=self.tool_registry.get_tool_definitions(),
            store=True
        )

        previous_response = initial_response
        parsed_response = utils.parse_response(previous_response)
        
        final_result = None
        final_response = None
        
        while True:
            
            # 检查是否有推理结果, 拼接parsed_response["reasoning"]中的所有内容
            if parsed_response["reasoning"]:
                reasoning = "".join(parsed_response["reasoning"])
                logger.debug(f"reasoning: {reasoning}")

            # 检查是否有最终消息, 拼接parsed_response["message"]中的所有内容
            

            # 检查是否有工具调用
            if parsed_response["function_call"]:
                tool_name = parsed_response["function_call"][0].name
                tool_args = json.loads(parsed_response["function_call"][0].arguments)
                tool_call_id = parsed_response["function_call"][0].id
                logger.info(f"calling tool with tool_name: {tool_name}, tool_args: {tool_args}")
                tool_result = self.tool_registry.call_tool(tool_name, **tool_args)
                logger.info(f"tool_result: {tool_result}")
                input_messages=[
                    {
                        "type": "function_call_output",
                        "call_id": tool_call_id,
                        "output": json.dumps(tool_result, ensure_ascii=False)
                    }
                ]
                
                # 调用Responses API - 符合API文档的请求结构
                response = self.client.responses.create(
                    previous_response_id=previous_response.id,
                    model="doubao-seed-1-6-251015",
                    input=input_messages,
                    tools=self.tool_registry.get_tool_definitions(),
                    store=True
                )
                previous_response = response
                parsed_response = utils.parse_response(previous_response)
            elif parsed_response["has_message"]:
                final_response = "".join(parsed_response["message"])
                logger.info(f"final_response: {final_response}")
                break
            else:
                logger.error(f"unexpected response, no message or function_call found: {parsed_response}")
                raise ValueError(f"unexpected response, no message or function_call found: {parsed_response}")
        
        # 如果达到最大迭代次数仍未生成最终结果，返回当前状态
        
        final_result = {
            "user_input": user_input,
            "final_response": final_response
        }
        
        return final_result

    