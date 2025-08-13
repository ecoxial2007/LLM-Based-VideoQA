from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
    base_url=""
)

# 非流式响应
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)

def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    result_messages = ''
    for chunk in stream:
        try:
            if chunk.choices[0].delta.content is not None:
                # print(chunk.choices[0].delta.content, end="")
                result_messages += chunk.choices[0].delta.content
        except:
            pass
    return result_messages

# if __name__ == '__main__':
#     messages = [{'role': 'user', 'content': '鲁迅和周树人的关系'},]
#     # 非流式调用
#     # gpt_35_api(messages)
#     # 流式调用
#     gpt_35_api_stream(messages)
