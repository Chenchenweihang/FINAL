import os
from datetime import datetime
from random import randint
from gradio_client import Client
import requests
from pathlib import Path

# 设置包含授权 Cookie 的请求头
headers = {
    "Cookie": "Authorization=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1MTI3NTkwMTExMSIsImlhdCI6MTcyODU0MTgxOSwiZXhwIjoxNzI4NzE0NjE5fQ.9umc8uQVlVAvPWM79AZUn1e7WtHP5Dzp2DsicNshqHw"
}
# 为 requests 库设置 cookies，包含相同的授权令牌
cookies = {
    "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1MTI3NTkwMTExMSIsImlhdCI6MTcyODU0MTgxOSwiZXhwIjoxNzI4NzE0NjE5fQ.9umc8uQVlVAvPWM79AZUn1e7WtHP5Dzp2DsicNshqHw"
}

# 使用服务器 URL 和请求头初始化 Gradio 客户端
client = Client("http://59.78.189.139:8082/",
                headers=headers,
                download_files=False  # 禁用自动文件下载
                )

# 定义从文本生成语音音频的函数
def speak_school(prompt: str, duration_s=5, guidance_scale=5, quality=3, seed=-1):
    # 如果没有提供种子，则生成一个随机种子
    if seed < 0:
        seed = randint(1, (1 << 31) - 1)

    # 调用 API 根据提供的参数预测音频
    audio_path = client.predict(
        prompt,
        duration_s,
        guidance_scale,
        seed,
        quality,
        api_name="/text2audio"  # 指定文本到音频转换的 API 端点
    )

    # 构建用于获取音频文件的 URL
    file_dir = "http://59.78.189.139:8082/file="
    remote_path = audio_path[0]["name"]  # 从响应中获取音频文件的名称
    print(remote_path)  # 打印远程路径以便调试

    # 创建完整的文件 URL
    file_path = file_dir + remote_path

    # 使用 requests 库下载音频文件
    response = requests.get(file_path, cookies=cookies)  # 发送 GET 请求获取音频文件
    response.raise_for_status()  # 如果请求不成功则引发错误

    # 根据当前时间戳生成文件名
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".mp4"

    # 定义用于在本地保存音频文件的输出目录
    output_dir = "./static/audio/"
    local_path = Path(output_dir + filename)  # 创建输出文件的 Path 对象

    # 确保输出目录存在
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # 将下载的内容写入本地文件
    with local_path.open('wb') as f:
        f.write(response.content)  # 将响应内容写入文件

    # 返回保存的音频文件相对于静态文件夹的路径
    return os.path.join('audio', filename)


# 脚本的入口点
if __name__ == '__main__':
    # 使用示例提示调用 speak_school 函数并打印结果
    print(speak_school('talking people, in restaurant'))  # 调用函数生成音频并输出结果
