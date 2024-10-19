from flask import Flask, render_template, request, jsonify, url_for
import os
from word2picture import gen_pic
from deepseek_api import send_message_to_deepseek
import threading

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

@app.route('/get_text_response', methods=['POST'])
def get_text_response():
    user_input = request.json.get('user_input')
    print(user_input)

    chatgpt_response = send_message_to_deepseek(user_input)
    description, option1, option2 = parse_response(chatgpt_response)

    response = {
        'description': description,
        'option1': option1,
        'option2': option2
    }
    return jsonify(response)

@app.route('/get_image', methods=['POST'])
def get_image():
    prompt = request.json.get('prompt')
    image_file_path = gen_pic(prompt)
    image_file_path = image_file_path.replace("\\", "/")
    image_url = url_for('static', filename=image_file_path, _external=True)

    return jsonify({'image_url': image_url})

@app.route('/get_audio', methods=['POST'])
def get_audio():
    prompt = request.json.get('prompt')
    # 这里应该是生成音频的代码，现在只是返回一个固定的音频URL
    audio_url = "static/audio/20241011155852.mp3"

    return jsonify({'audio_url': audio_url})

def parse_response(response_text):  # {{ 新增函数：解析响应内容 }}
    lines = response_text.split('\n')
    description = lines[0].strip().rstrip('。') if len(lines) > 0 else ''
    option1 = ''
    option2 = ''
    for line in lines[1:]:
        if line.startswith('选项一：'):
            option1 = line.replace('选项一：', '').strip()
        elif line.startswith('选项二：'):
            option2 = line.replace('选项二：', '').strip()
    return description, option1, option2

if __name__ == "__main__":  # 当文件作为主程序运行时
    app.run(port=3000)  # 启动Flask应用，监听3000端口
