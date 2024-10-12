from openai import OpenAI
import io
import contextlib

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key="sk-cbd03dd9233e47c29328e4d34f945fa5", base_url="https://api.deepseek.com/")

messages = [{"role": "system", "content": "你是一个中文的机器人，擅长进行学习任务单的生成，而且你生成的任务单中每个大小标题都需要加粗,但是聊天的时候不需要加粗，当且仅当得到有关于学习任务的要求的时候才进行任务单的生成"}]

# 根据用户选择确定预设的初始系统消息
def generate_system_message(learning_goal, learning_background, task_type, tech_resources, feedback_type):
    # CO-STAR 框架的各个部分定义
    context = "你是一个中文的机器人，擅长进行学习任务单的生成，而且你生成的任务单中每个大小标题都需要加粗,但是聊天的时候不需要加粗，当且仅当得到有关于学习任务的要求的时候才进行任务单的生成"

    # 回答的格式
    additional_prompt = (
        "请根据以下要求进行回答。"
        " 输出结果必须以 JSON 格式提供，并且提取输出内容中的关键词。"
        " 请按照以下固定格式进行输出：\n"
        "```json\n"
        "{\n"
        '  "task": "描述任务内容",\n'
        '  "output": "模型生成的完整输出内容",\n'
        '  "keywords": ["关键词1", "关键词2", "关键词3", ...]\n'
        "}\n"
        "```"
    )

    # 拼接到原有的 content 中
    context += f" {additional_prompt}"
    context += " 你需要根据用户下面选择的内容生成定制化的学习任务。"
    # 根据学习目标选择（明确型、激励型、稳定型、高效型）
    if learning_goal == "明确型":
        observation = "你需要帮助学生明确具体的学习目标，生成有条理的学习任务清单，确保每个步骤都有清晰的描述和预期成果。"
    elif learning_goal == "激励型":
        observation = "你需要通过提供激励性任务来激发学生的学习兴趣，鼓励他们通过小胜利逐步实现更大的目标。"
    elif learning_goal == "稳定型":
        observation = "你需要为学生设计出能够长期稳定执行的任务，帮助他们保持均衡的学习进度，避免过度学习或疲劳。"
    elif learning_goal == "高效型":
        observation = "你需要帮助学生优化学习过程，优先处理关键任务，通过高效策略帮助他们在最短的时间内完成更多的学习内容。"

    # 根据学习背景选择（童话型、现实型、科幻型、实用型）
    if learning_background == "童话型":
        situation = "你需要将学习内容融入童话故事中，帮助学生通过故事中的角色和情节理解学习任务。"
    elif learning_background == "现实型":
        situation = "你需要通过现实生活中的场景设计学习任务，使学生能够将所学知识应用于日常生活中。"
    elif learning_background == "科幻型":
        situation = "你需要通过未来技术和科幻情节为学生构建学习情境，激发他们的创造力和想象力。"
    elif learning_background == "实用型":
        situation = "你需要帮助学生将学习任务与实用技能相结合，确保他们能够立即将知识应用于工作或生活中。"

    # 根据任务类型选择（操作型课堂任务、讲授型课堂任务、理解型课堂任务）
    if task_type == "操作型课堂任务":
        task = "你需要生成包含具体操作步骤的学习任务，帮助学生通过动手实践掌握技能。"
    elif task_type == "讲授型课堂任务":
        task = "你需要设计以讲解为主的任务，确保学生能够系统理解所学理论知识，并能够复述和应用。"
    elif task_type == "理解型课堂任务":
        task = "你需要生成引导学生进行深度思考和批判性理解的任务，帮助他们在知识点之间建立联系。"

    # 根据技术和资源选择（AI工具、电子游戏、传统工具、不使用工具）
    if tech_resources == "AI工具":
        action = "你可以使用AI工具来辅助学生完成任务，例如生成学习内容、解答疑问或提供个性化学习建议。"
    elif tech_resources == "电子游戏":
        action = "你需要将学习任务设计成游戏化的形式，使用电子游戏中的机制激发学生的学习动力。"
    elif tech_resources == "传统工具":
        action = "你需要依靠传统工具来辅助学生学习，提供需要手动完成的任务，如写作、计算或阅读。"
    elif tech_resources == "不使用工具":
        action = "你需要生成任务，不依赖任何外部工具，帮助学生通过独立思考和问题解决完成学习。"

    # 根据评估反馈选择（学生反馈方式、教师评估方式、教师自评方式）
    if feedback_type == "学生反馈方式":
        result = "你需要帮助学生通过自我反馈机制评估自己的学习进展，并根据他们的反馈调整学习任务。"
    elif feedback_type == "教师评估方式":
        result = "你需要生成允许教师进行评价的任务，并根据教师的反馈调整学习策略和内容。"
    elif feedback_type == "教师自评方式":
        result = "你需要帮助教师通过自我评估机制反思他们的教学方式，并据此进行改进。"

    # 生成最终的系统消息
    system_message = {
        "role": "system",
        "content": f"{context} {observation} {situation} {task} {action} {result}"
    }

    return system_message


# 示例使用
#learning_goal = "高效型"
#learning_background = "现实型"
#task_type = "理解型课堂任务"
#tech_resources = "AI工具"
#feedback_type = "教师评估方式"

#system_message = generate_system_message(learning_goal, learning_background, task_type, tech_resources, feedback_type)
#print(system_message)


def send_message_to_deepseek(userInput):
    chat_output = f"You: {userInput}\n"
    print(chat_output)
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
