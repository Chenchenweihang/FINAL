from flask import Flask, render_template, request, jsonify, url_for
import os
from word2picture import gen_pic
from deepseek_api import send_message_to_deepseek, reset_messages  # 导入 reset_messages 函数
from sund_api import get_sund_music
import threading

# 创建一个Flask应用实例
app = Flask(__name__)

# 配置静态文件夹路径
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/')  # 定义根路径的路由
def index():
    return render_template('index.html')  # 渲染index.html模板页面

@app.route('/get_text_response', methods=['POST'])
def get_text_response():
    user_input = request.json.get('user_input')
    print(user_input)

    chatgpt_response = send_message_to_deepseek(user_input)
    description, option1, option2 = parse_response(chatgpt_response)

    # 定义何时游戏结束的逻辑
    # 例如，当描述中包含某个关键词，或者选项中有特定的内容
    game_over = False
    end_game_keywords = ['游戏结束', '结束', '终点']  # 根据需求定义关键词

    for keyword in end_game_keywords:
        if keyword in description:
            game_over = True
            break


    response = {
        'description': description,
        'option1': option1,
        'option2': option2,
        'game_over': game_over  # 添加game_over标志
    }
    return jsonify(response)

@app.route('/get_image', methods=['POST'])
def get_image():
    prompt = request.json.get('prompt')
    print(prompt)
    image_file_path = gen_pic(prompt)
    image_file_path = image_file_path.replace("\\", "/")
    image_url = url_for('static', filename=image_file_path, _external=True)

    return jsonify({'image_url': image_url})

@app.route('/get_audio', methods=['POST'])
def get_audio():
    prompt = request.json.get('prompt')
    # 这里应该是生成音频的代码，现在只是返回一个固定的音频URL
    audio_url = "static/audio/20241011155852.mp3"
    # audio_url = get_sund_music(prompt, '1')

    return jsonify({'audio_url': audio_url})

@app.route('/end_game', methods=['POST'])
def end_game():
    reset_messages()  # 调用重置 messages 的函数
    return jsonify({'status': 'success', 'message': '游戏已结束，消息已清空。'})


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
