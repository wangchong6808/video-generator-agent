from typing import Optional
from volcenginesdkarkruntime import Ark
import time


class VideoGeneratorTool:
    """视频生成工具"""
    
    def __init__(self, client: Ark):
        """
        初始化视频生成工具
        
        Args:
            client: Ark客户端实例
        """
        self.client = client
        self.model = "doubao-seedance-1-0-pro-250528"  # 使用火山引擎推荐的视频生成模型
    
    def generate(self, prompt: str, duration: int = 5, resolution: str = "720P") -> str:
        """
        根据提示词生成视频
        
        Args:
            prompt: 视频生成提示词
            duration: 视频时长（秒），默认5秒
            resolution: 视频分辨率，默认720P
            
        Returns:
            生成的视频URL
        """
        # 添加视频生成参数到提示词中
        prompt_with_params = f"{prompt} --duration {duration} --resolution {resolution}"
        
        # 创建视频生成任务
        create_result = self.client.content_generation.tasks.create(
            model=self.model,
            content=[
                {
                    "type": "text",
                    "text": prompt_with_params
                }
            ]
        )
        
        # 获取任务ID
        task_id = create_result.id
        
        # 轮询查询任务状态
        while True:
            get_result = self.client.content_generation.tasks.get(task_id=task_id)
            status = get_result.status
            
            if status == "succeeded":
                # 任务成功，提取视频URL
                video_url = get_result.content.video_url
                return video_url
            elif status == "failed":
                # 任务失败，抛出异常
                raise Exception(f"视频生成失败: {get_result.error}")
            else:
                # 任务正在进行中，等待10秒后继续查询
                time.sleep(10)
