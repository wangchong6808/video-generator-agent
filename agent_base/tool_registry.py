from typing import Any, Callable, Dict, List, Optional, Union
from volcenginesdkarkruntime import Ark


class ToolRegistry:
    """工具注册器，用于管理和执行所有可用工具"""
    
    def __init__(self, client: Ark):
        """
        初始化工具注册器
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.tools: Dict[str, Callable] = {}
        self.tool_definitions = []

    
    
    def register_tools(self, tool: Callable, tool_definition: Dict):
        """
        注册所有工具
        """
        tool_name = tool_definition["name"]
        self.tools[tool_name] = tool
        self.tool_definitions.append(tool_definition)
    
    def get_tool_definitions(self) -> List[Dict]:
        """
        获取所有工具定义
        
        Returns:
            工具定义列表
        """
        return self.tool_definitions
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        调用指定工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            工具调用结果
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not registered")
        
        return self.tools[tool_name](**kwargs)
