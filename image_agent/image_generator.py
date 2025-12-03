from typing import Optional
from volcenginesdkarkruntime import Ark


class ImageGeneratorTool:
    """图片生成工具"""
    
    def __init__(self, client: Ark):
        """
        初始化图片生成工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seedream-4-0-250828"
    
    def generate(self, prompt: str, size: str = "1024x1024", watermark: bool = False) -> str:
        """
        根据提示词生成图片
        
        Args:
            prompt: 图片生成提示词
            size: 图片尺寸，默认1024x1024
            watermark: 是否添加水印，默认False
            
        Returns:
            生成的图片URL
        """
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            watermark=watermark,
            response_format="url"
        )
        
        # 提取图片URL
        image_url = response.data[0].url
        return image_url
