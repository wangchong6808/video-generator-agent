import os
from typing import List, Dict, Any
from pydantic import BaseModel
from volcenginesdkarkruntime import Ark

class ImageCheckRequest(BaseModel):
    """
    图片检查请求参数
    """
    prompt: str  # 生成图片的提示词
    image_url: str  # 图片URL

class ImageCheckResult(BaseModel):
    """
    图片检查结果
    """
    is_compliant: bool  # 是否符合要求
    message: str  # 检查结果描述
    issues: List[str] = []  # 不符合要求的具体问题


def image_check(prompt: str, image_url: str) -> Dict[str, Any]:
    """
    调用doubao-seed-1-6-251015模型检查图片是否符合提示词要求
    
    Args:
        prompt: 生成图片的提示词
        image_url: 图片URL
        
    Returns:
        检查结果，包含是否符合要求、描述和具体问题
    """
    try:
        # 创建Ark客户端
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=os.getenv('VOLC_APIKEY', ''),
        )
        
        # 构建消息
        messages = [
            {
                "role": "user",
                "content": [
                    # 图片信息
                    {"type": "image_url", "image_url": {"url": image_url}},
                    # 文本消息，要求模型检查图片是否符合提示词
                    {
                        "type": "text", 
                        "text": f"请检查这张图片是否符合以下提示词要求：{prompt}\n\n评估维度：\n- 主体：图片中的主要对象是否为一只狗\n- 场景：图片的背景和环境是否与提示词描述一致\n- 风格：图片的艺术风格是否与提示词描述一致\n- 细节：图片的细节表现是否与提示词描述一致\n- 氛围：图片的整体氛围是否与提示词描述一致\n\n请按照以下格式返回结果：\n是否符合要求：[是/否]\n描述：[简要描述图片内容]\n具体问题：[如果不符合要求，列出具体问题，否则留空]\n"}
                        #"text": f"请检查这张图片是否符合以下提示词要求：{prompt}\n\n评估维度：\n- 主体：图片中的主要对象是否与提示词描述一致\n- 场景：图片的背景和环境是否与提示词描述一致\n- 风格：图片的艺术风格是否与提示词描述一致\n- 细节：图片的细节表现是否与提示词描述一致\n- 氛围：图片的整体氛围是否与提示词描述一致\n\n请按照以下格式返回结果：\n是否符合要求：[是/否]\n描述：[简要描述图片内容]\n具体问题：[如果不符合要求，列出具体问题，否则留空]\n"}
                ],
            }
        ]
        
        # 调用模型
        completion = client.chat.completions.create(
            model="doubao-seed-1-6-251015",
            messages=messages,
        )
        
        # 解析模型回复
        response_content = completion.choices[0].message.content
        
        # 处理回复内容
        lines = response_content.strip().split('\n')
        is_compliant = False
        description = ""
        issues = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("是否符合要求："):
                is_compliant = line.split("：")[1].strip() == "是"
            elif line.startswith("描述："):
                description = line.split("：", 1)[1].strip()
            elif line.startswith("具体问题："):
                issues_str = line.split("：", 1)[1].strip()
                if issues_str:
                    issues = [issue.strip() for issue in issues_str.split("、")]
        
        # 返回结果
        return {
            "is_compliant": is_compliant,
            "message": description,
            "issues": issues
        }
    
    except Exception as e:
        # 处理异常
        return {
            "is_compliant": False,
            "message": f"检查图片时发生错误：{str(e)}",
            "issues": [f"检查图片时发生错误：{str(e)}"]
        }
