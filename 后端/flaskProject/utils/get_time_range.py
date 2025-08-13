import json
import re


# 将时间字符串转换为秒数的函数
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s


def convert_time_range(time_range):
    # 分割起始时间和结束时间
    start_time, end_time = time_range.split('-')

    # 如果时间长度不足 8 个字符，补充 '00:' 表示小时
    if len(start_time) == 5:  # 只有分和秒，补充 '00:'
        start_time = '00:' + start_time
    if len(end_time) == 5:  # 只有分和秒，补充 '00:'
        end_time = '00:' + end_time

    # 返回格式化后的时间段
    return f"[{start_time}-{end_time}]"

# 提取类似 [00:03:54-00:13:55] 的内容并转换为 annotations 结构
def extract_time_ranges(text, total_duration):
    annotations = []
    time_pattern = r"(\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?)-(\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?)"

    # 匹配所有的时间段
    matches = re.findall(time_pattern, text)
    print(matches)

    for start_time, end_time in matches:
        # 将时间转换为秒
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)

        # 将秒数转换为比例
        start_ratio = start_seconds / total_duration
        end_ratio = end_seconds / total_duration

        # 生成annotation字典（这里颜色可以随机分配或预先定义）
        annotation = {
            'start': start_ratio,
            'end': end_ratio,
            'color': '#f00'  # 颜色可根据需求调整
        }

        annotations.append(annotation)

    return annotations



def get_duration(video_name):
    with open('./data/video_length.json', 'r') as f:
        duration_dict = json.load(f)
    return duration_dict[video_name]

