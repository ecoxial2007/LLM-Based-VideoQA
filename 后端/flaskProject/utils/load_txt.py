import re
import os
import json
import pandas as pd
def read_txt_to_list(file_path):
    """
    逐行读取指定的txt文件，并将内容存入列表中。
    每行格式为：[时间段] 文本
    结果列表格式为：[[文本], [时间段], [文本], [时间段], ...]

    Args:
        file_path (str): txt文件的路径

    Returns:
        list: 包含文本和时间段的列表
    """
    result = []

    # 定义正则表达式模式，用于提取时间段和文本
    pattern = re.compile(r'\[(.*?)\]\s*(.*)')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    # 跳过空行
                    continue
                match = pattern.match(line)
                if match:
                    time_range = match.group(1)
                    text = match.group(2)
                    result.append({'time_range': time_range,
                                   'text': text})
                else:
                    print(f"警告：第 {line_num} 行不符合预期格式，内容：{line}")
                    # 根据需求决定如何处理不符合格式的行
                    # 这里将整个行作为文本添加
                    result.append({'error': line})
        return result
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到。")
        return []
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return []

def get_file_name_without_extension(file_path):
    # 提取文件名（包含扩展名）
    file_name_with_extension = os.path.basename(file_path)
    # 移除扩展名
    file_name = os.path.splitext(file_name_with_extension)[0]
    return file_name

def extract_video_name(text):
    pattern = r"\d+_\d+_\d+"
    matches = re.findall(pattern, text)
    return matches



def load_video_name_mapping(json_path):
    """
    读取 JSON 文件，返回一个字典映射原始视频名称到重命名后的名称。

    Args:
        json_path (str): JSON 文件路径

    Returns:
        dict: 映射字典
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        return mapping
    except FileNotFoundError:
        print(f"错误：文件 {json_path} 未找到。")
        return {}
    except json.JSONDecodeError:
        print(f"错误：文件 {json_path} 不是有效的 JSON 格式。")
        return {}
    except Exception as e:
        print(f"读取 JSON 文件时发生错误：{e}")
        return {}


def get_mapped_video_list(video_paths, mapping):
    """
    获取视频目录下所有 .mp4 文件，并根据映射字典进行重命名。

    Args:
        video_dir (str): 视频目录路径
        mapping (dict): 原始名称到重命名的映射字典

    Returns:
        pd.DataFrame: 包含重命名后的视频名称和视频路径的 DataFrame
    """

    # 创建映射后的列表
    mapped_videos = []
    for path in video_paths:
        base_name = os.path.splitext(os.path.basename(path))[0]  # 获取不带扩展名的文件名
        if base_name in mapping:
            renamed = mapping[base_name]
        else:
            renamed = base_name  # 如果没有映射，保留原名
        mapped_videos.append({"重命名后名称": renamed, "视频路径": path})

    # 创建 DataFrame
    video_df = pd.DataFrame(mapped_videos)
    return video_df