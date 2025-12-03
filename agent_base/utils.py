# 工具函数
import os
from typing import Dict
from loguru import logger

def get_api_key():
    """获取API密钥"""
    api_key = os.getenv('ARK_API_KEY')
    if not api_key:
        raise ValueError("ARK_API_KEY环境变量未配置")
    return api_key

def parse_response(response: object) -> Dict:
        """
        解析API响应，提取工具调用结果和最终消息
        
        Args:
            response: API响应字典
            
        Returns:
            包含是否有函数调用、具体问题和改进建议的元组
        """
        
        parsed_response = {
            "has_function_call": False,
            "has_reasoning": False,
            "has_message": False,
            "reasoning": [],
            "function_call": [],
            "message": []
        }
        for item in response.output:
            if item.type == "reasoning":
                parsed_response["has_reasoning"] = True
                parsed_response["reasoning"].append(item.summary[0].text)
            elif item.type == "function_call":
                parsed_response["has_function_call"] = True
                parsed_response["function_call"].append(item)
                # {
                #     "arguments": "{\"location\":\"北京\"}",
                #     "call_id": "call_****a6al",
                #     "name": "获取天气信息",
                #     "type": "function_call",
                #     "id": "fc_0217****c976b",
                #     "status": "completed"
                # }
            elif item.type == "message":
                parsed_response["has_message"] = True
                parsed_response["message"].append(item.content[0].text)
        # print(f"parsed_response: {parsed_response}")
        logger.debug(f"parsed_response: {parsed_response}")
        return parsed_response