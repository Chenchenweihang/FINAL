import base64  # 导入base64库用于解码图像数据
import os  # 导入os库用于操作文件和目录
from datetime import datetime  # 导入datetime库获取当前日期时间

import requests  # 导入requests库用于发送HTTP请求


def pic(prompt, url="http://59.78.189.139:8081", steps=10,
        authorization_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1MTI3NTkwMTExMSIsImlhdCI6MTcyODU0MTgxOSwiZXhwIjoxNzI4NzE0NjE5fQ.9umc8uQVlVAvPWM79AZUn1e7WtHP5Dzp2DsicNshqHw"):
    """
    生成图像的函数，使用指定的API请求生成基于提示词的图像。

    参数：
    - prompt: 用于生成图像的提示文本。
    - url: API的URL，默认为指定的URL。
    - steps: 图像生成过程中的步骤数，默认为10。
    - authorization_token: 用于API认证的令牌。

    返回：
    - 生成图像的文件路径（相对路径），或失败消息。
    """

    # 准备要发送的JSON负载数据
    payload = {
        "prompt": prompt,  # 传入的提示词
        "steps": steps  # 生成图像的步骤数
    }

    # 设置请求的cookies，包含认证信息
    cookies = {
        "Authorization": authorization_token  # 使用传入的认证令牌
    }

    # 发送POST请求到指定的URL，传递负载数据和cookies（认证信息）
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload, cookies=cookies)

    # 将返回的响应内容转为JSON格式
    r = response.json()

    # 检查返回的数据是否包含'images'字段，如果没有则返回失败消息
    if 'images' not in r or not r['images']:
        return "请求失败或返回数据无效"  # 如果返回数据无效，给出提示信息

    # 如果返回数据有效，解码并保存图像
    # 生成文件名，使用当前的日期时间来命名，避免文件名重复
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"  # 文件名格式为"YYYYMMDDHHMMSS.png"

    # 设置保存图像的文件夹路径
    save_dir = "static/image"  # 保存图像的文件夹，可以根据需求调整路径
    save_path = os.path.join(save_dir, filename)  # 生成完整的文件路径

    # 确保保存图像的目录存在，如果没有则创建它
    os.makedirs(save_dir, exist_ok=True)  # exist_ok=True表示如果目录已经存在，不会抛出错误

    # 打开文件并将解码后的图像数据写入文件
    with open(save_path, 'wb') as f:  # 以二进制写入模式打开文件
        f.write(base64.b64decode(r['images'][0]))  # 解码base64格式的图像数据并保存为文件

    # 返回保存的图像文件路径，用户可以用来访问该图像
    return os.path.join('image', filename)  # 返回相对路径（以供Web服务器使用）


# 使用示例：调用pic函数生成一张“Lamborghini”图像，并获取保存路径
result_path = pic("a Lamborghini")  # 传入提示词"Lamborghini"
print(result_path)  # 打印返回的图像保存路径
