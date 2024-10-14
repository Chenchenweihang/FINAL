from openai import OpenAI
import io
import contextlib

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key="sk-cbd03dd9233e47c29328e4d34f945fa5", base_url="https://api.deepseek.com/")

messages = [{'role': 'system',
            'content': '你是文字游戏的控制者，现在我在开车兜风，会遇到很多风景不同的岔路，岔路后面还会有岔路，每次遇到岔路你将给我选项1和选项2两个选项代表选择不同的岔路，接下来的风景要根据我的选择进行生成，每一段字数控制在50字以内。生成的格式为一段描述文字，换行，选项一：选项一的内容，选项二：选项二的内容',}]
def send_message_to_deepseek(userInput):
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
        messages.append({"role": "user", "content": response.choices[0].message.content})
        chat_output += f"System: {bot_response}\n"
    except Exception as e:
        chat_output += f"Error: {str(e)}\n"
        bot_response = "An error occurred while communicating with the API."
    # print(chat_output)
    return bot_response
