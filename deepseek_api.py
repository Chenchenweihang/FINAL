from openai import OpenAI
import io
import contextlib
import random

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key="sk-cbd03dd9233e47c29328e4d34f945fa5", base_url="https://api.deepseek.com/")
MAX_ROUNDS = random.randint(10, 15)
messages = [{'role': 'system',
'content': f'你是文字游戏的控制者，现在我在开车兜风，会遇到很多风景不同的岔路，岔路后面还会有岔路。游戏将在{MAX_ROUNDS}轮对话后结束。在每次遇到岔路时，你将提供选项1和选项2两个选项，代表选择不同的岔路。根据我的选择生成接下来的风景描述，每段字数控制在50字以内。生成的格式为一段描述文字，换行，选项一：选项一的内容，选项二：选项二的内容。当达到{MAX_ROUNDS}轮时，游戏需要结束，所以你需要保持适当的游戏节奏，保证能够在{MAX_ROUNDS}轮对话后结束游戏，输出游戏结束的消息。'}]

length = 0

def send_message_to_deepseek(userInput):
    global messages
    global length
    # 计算当前轮次数
    # 初始系统消息为1条，每轮对话添加2条（用户和系统）
    current_round = (len(messages) - 1) // 2
    if userInput == "欢迎来到冒险游戏！":
        print("现在开始游戏了")
        messages = [{'role': 'system',
                     'content': f'你是文字游戏的控制者，现在我在开车兜风，会遇到很多风景不同的岔路，岔路后面还会有岔路。游戏将在{MAX_ROUNDS}轮对话后结束。在每次遇到岔路时，你将提供选项1和选项2两个选项，代表选择不同的岔路。根据我的选择生成接下来的风景描述，每段字数控制在50字以内。生成的格式为一段描述文字，换行，选项一：选项一的内容，选项二：选项二的内容。当达到{MAX_ROUNDS}轮时，游戏需要结束，所以你需要保持适当的游戏节奏，保证能够在{MAX_ROUNDS}轮对话后结束游戏，输出游戏结束的消息。'}]

    chat_output = f"You: {userInput}\n"
    # print(chat_output)
    messages.append({"role": "user", "content": userInput})
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            stream=False
        )
        bot_response = response.choices[0].message.content
        # 检查是否达到最后一轮

        # 添加系统消息
        messages.append({"role": "system", "content": response.choices[0].message.content})
        length += 1
        print(length)
        print(messages)
        chat_output += f"System: {bot_response}\n"
    except Exception as e:
        chat_output += f"Error: {str(e)}\n"
        bot_response = "An error occurred while communicating with the API."
    # print(chat_output)
    return bot_response


def reset_messages():
    global messages
    global length
    messages = [initial_message]
    length = 0
    print("messages 已被重置。")
