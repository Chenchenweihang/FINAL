from flask import Flask, render_template, request, jsonify, url_for
import os
import openai

import sund_api
from word2picture import gen_pic
from deepseek_api import send_message_to_deepseek

# 创建一个Flask应用实例
app = Flask(__name__)

# 配置静态文件夹路径
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# # 设置OpenAI API密钥
# openai.api_key = 'YOUR_OPENAI_API_KEY'  # 需要替换为实际的API密钥
# client = openai.OpenAI(
#     api_key="sk-R5TQYS8iZneCnAGQQnIVYw",  # 示例API密钥，请替换为实际的API密钥
#     base_url="http://59.78.189.138:8000"  # OpenAI API的服务器地址
# )
#
# # 定义游戏控制者的聊天历史
# chat_history = [  # 游戏控制者的初始消息历史
#     {"role": "system",
#      "content": "你是文字游戏的控制者，现在我在开车兜风，会遇到很多风景不同的岔路，岔路后面还会有岔路，每次遇到岔路你将给我选项1和选项2两个选项代表选择不同的岔路，接下来的风景要根据我的选择进行生成，每一段字数控制在50字以内。"},
#     {"role": "user", "content": "我开着车在沿海公路上疾驰。"},  # 初始用户输入
# ]
#
# def generate_chat_response(messages):
#     # 调用OpenAI API生成响应
#     response = client.chat.completions.create(
#         model="yi",  # 请替换为实际使用的模型名称
#         messages=messages  # 输入的消息列表
#     )
#     return response.choices[0].message.content.strip()  # 返回生成的响应内容，去除首尾空格

@app.route('/')  # 定义根路径的路由
def index():
    return render_template('index.html')  # 渲染index.html模板页面

@app.route('/get_response', methods=['POST'])  # 定义处理POST请求的路由
def get_response():
    user_input = request.json.get('user_input')  # 从请求中获取用户输入
    # chat_history.append({"role": "user", "content": user_input})  # 将用户输入添加到聊天历史中
    print(user_input)  # 打印用户输入以便于调试

    chatgpt_response = send_message_to_deepseek(user_input)  # 生成GPT的响应
    # chat_history.append({"role": "assistant", "content": chatgpt_response})  # 将助手的响应添加到聊天历史中

    print(chatgpt_response)  # 打印GPT生成的响应以便于调试
    # demo of response
    # 你驶入一条蜿蜒的山路，前方出现两条岔路。
    #
    # 选项1：左转，进入一片茂密的森林。
    # 选项2：右转，沿着山脊前行，视野开阔。


    # # 使用chatgpt_response生成音频文件并获取其路径
    # audio_file_path = speak_school(chatgpt_response)
    # audio_file_path = audio_file_path.replace("\\", "/")  # 替换文件路径中的反斜杠以兼容URL格式
    # audio_url = url_for('static', filename=audio_file_path, _external=True)  # 生成音频文件的URL
    style = "happy"
    audio_url = sund_api.get_sund_music(chatgpt_response,style)


    # 使用chatgpt_response生成图片文件并获取其路径
    image_file_path = gen_pic(chatgpt_response)
    image_file_path = image_file_path.replace("\\", "/")  # 替换文件路径中的反斜杠以兼容URL格式
    image_url = url_for('static',filename=image_file_path, _external=True)  # 生成图片文件的URL

    # 准备返回的响应内容
    response = {
        'chatgpt_response': chatgpt_response,  # GPT生成的文本响应
        'image_url': image_url,  # 图片文件的URL
        'audio_url': audio_url  # 音频文件的URL
    }
    return jsonify(response)  # 返回JSON格式的响应

if __name__ == "__main__":  # 当文件作为主程序运行时
    app.run(port=3000)  # 启动Flask应用，监听3000端口
