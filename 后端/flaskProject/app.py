import glob
import os

from flask import Flask, request, jsonify, send_from_directory

from utils.call_gpt import gpt_35_api_stream
from utils.get_time_range import get_duration, extract_time_ranges
from utils.load_txt import read_txt_to_list, load_video_name_mapping, get_mapped_video_list

app = Flask(__name__)


# 视频列表API
@app.route('/videos', methods=['GET'])
def get_videos():
    video_list = glob.glob(os.path.join('data/video', '*.mp4'))
    video_mapping = load_video_name_mapping('./data/video_name.json')
    video_df = get_mapped_video_list(video_list, video_mapping)
    return jsonify({os.path.splitext(os.path.basename(video['视频路径']))[0]: video['重命名后名称'] for video in
                    video_df.to_dict(orient='records')})


# 视频文件路由
@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('data/video', filename)


# 根据问题检索视频的函数
def find_video_name(mapping, question):
    dict2str = {}
    for k, v in mapping.items():
        if isinstance(v, str):
            dict2str[k] = v

    prompt = (
            "我将给你一个C语言相关的问题，以及一串视频列表，列表储存为文件名：内容简介。"
            "请根据问题内容找到对应视频，并给我数字格式的文件名（例如：x_x_x）。"
            f"以下是问题：{question}\n"
            "视频列表：\n" + str(dict2str)
    )
    messages = [{'role': 'user', 'content': prompt}]

    # 传递给GPT API的完整对话历史
    response = gpt_35_api_stream(messages)
    response = response.strip()
    if '未找到相关视频' in response:
        return None
    return response


# GPT API 响应（流式）
@app.route('/gpt-response', methods=['POST'])
def gpt_response():
    data = request.json
    question = data.get('question')
    video_name = data.get('video_name')
    if not question:
        return jsonify({"error": "问题是必须的！"}), 400

    video_mapping = load_video_name_mapping('./data/video_name.json')
    if not video_name:
        # 如果未提供视频名称，尝试根据问题检索视频
        response_video_name = find_video_name(video_mapping, question)
        # 解析GPT返回的文件名
        video_name = response_video_name.strip() if response_video_name else None
        if not video_name or video_name not in video_mapping:
            return jsonify({"error": "未找到相关视频，请选择一个视频或重新提问。"}), 400

    # 加载PPT数据
    ppts = read_txt_to_list(os.path.join('data/ppt', video_name + '.txt'))

    # 构造给GPT的提示
    prompt = (
        "我希望你以一名C语言老师的身份来回答我的问题。"
        "我提供了授课视频中的内容和时间戳。请根据这些内容来回答问题，并在回答中返回相关的时间戳。"
        "尽量不要直接给出答案，以简洁友好的回复引导学生看视频。除非我说'直接告诉我答案',你再回答八进制的0100转成十六进制的答案并解释。"
        f"以下是授课视频的大致内容和时间戳：\n{ppts}"
    )
    messages = [{'role': 'user', 'content': prompt}, {'role': 'user', 'content': question}]
    response = gpt_35_api_stream(messages)
    # 提取时间戳
    video_path = os.path.join('data/video', video_name + '.mp4')
    if not os.path.exists(video_path):
        return jsonify({"error": "视频文件未找到。"}), 400
    total_duration = get_duration(video_name)
    annotations = extract_time_ranges(response, total_duration)

    return jsonify({
        "response": response,
        "video_name": video_name,
        "annotations": annotations,
        "total_duration": total_duration
    })


# 加载PPT API
@app.route('/load-ppt', methods=['GET'])
def load_ppt():
    video_name = request.args.get('video_name')
    if not video_name:
        return jsonify({"error": "视频名称是必须的！"}), 400
    ppts = read_txt_to_list(os.path.join('data/ppt', video_name + '.txt'))
    return jsonify({"ppts": ppts})


if __name__ == '__main__':
    app.run()
