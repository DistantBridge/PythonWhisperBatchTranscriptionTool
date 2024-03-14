import os
import whisper
import subprocess
import opencc

# ver1.5 加入中文的繁体转简体的功能。
# ver1.7 可以识别更多种音频文件。包括：mp3, flac, wav。
# 转写.aac文件时可能会报错，因此暂时用注释的方法取消了对aac文件的转写。

# 设置音频文件夹路径
audio_folder = "D:/Temp_Files/Whisper测试"
transcribed_files_log = "transcribed_files.log"

# 加载 Whisper 模型
def load_whisper_model(size: str):
    return whisper.load_model(size)

# 检测并返回已转写的文件名列表
def get_transcribed_files(log_path):
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            return file.read().splitlines()
    return []

# 检查并记录转写文件
def log_transcribed_file(log_path, file_name):
    with open(log_path, 'a') as file:
        file.write(f"{file_name}\n")

# 检测语言并转写音频
def transcribe_audio(audio_path, model_size='small'):
    model = load_whisper_model(model_size)
    result = model.transcribe(audio_path)
    return result

# 主执行函数
def process_audio_files(folder_path, log_path):
    # 获取已转写文件名列表（不包含扩展名）
    transcribed_files = set(os.path.splitext(file)[0] for file in get_transcribed_files(log_path))
    
    # 预处理：转换 .aac 文件为 .wav，仅当文件未出现在已转写列表中
    # preprocess_convert_aac_to_wav(folder_path, transcribed_files)
    
    supported_extensions = ['.mp3', '.flac', '.wav']  # 注意已移除 .aac

    for file in os.listdir(folder_path):
        audio_path = os.path.join(folder_path, file)  # 统一使用 audio_path
        file_extension = os.path.splitext(file)[1].lower()

        if file_extension not in supported_extensions:
            continue

        if file in transcribed_files:
            print(f"{file} has already been transcribed.")
            continue
        

        # 如果文件是 .aac 格式，先将其转换为 .wav，并更新 audio_path 变量
        if file_extension == '.aac':
            print(f"Converting {file} to WAV format.")
            audio_path = convert_aac_to_wav(audio_path)


        # 使用"base"模型进行快速语言检测
        language_detection_result = transcribe_audio(audio_path, 'base')
        detected_language = language_detection_result['language']
        
        # 根据检测到的语言选择模型
        if detected_language == 'en':
            final_result = transcribe_audio(audio_path, 'small')
        elif detected_language.startswith('zh'):
            final_result = transcribe_audio(audio_path, 'medium')
            segments = convert_segments_to_simplified(final_result['segments'])
            # 保存简体中文结果到新文件
            save_simplified_transcripts(audio_path, segments)
        else:
            print(f"Unsupported language {detected_language} for file {file}. Skipping transcription.")
            continue
        
        # 保存转写结果，并在每一句之间加入换行
        base_file_path = os.path.splitext(audio_path)[0]  # 去除扩展名
        text_file_path = f"{base_file_path}.txt"
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            for segment in final_result['segments']:
                text_file.write(segment['text'] + "\n")
        
        # 保存包含时间轴的转写结果
        timestamps_file_path = f"{base_file_path}_timestamps.txt"
        with open(timestamps_file_path, 'w', encoding='utf-8') as time_file:
            for segment in final_result['segments']:
                start = segment['start']
                end = segment['end']
                time_file.write(f"{start:.2f} - {end:.2f}: {segment['text']}\n")
        
        log_transcribed_file(log_path, file)
        print(f"Transcribed {file} successfully using the {detected_language} model.")

# 进行繁体到简体中文转换的函数
def save_simplified_transcripts(audio_path, segments):
    simplified_file_path = audio_path.replace(".mp3", "_simplified.txt")
    with open(simplified_file_path, 'w', encoding='utf-8') as f:
        for segment in segments:
            f.write(segment['text'] + "\n")

def convert_segments_to_simplified(segments):
    converter = opencc.OpenCC('t2s')
    simplified_segments = []
    for segment in segments:
        simplified_text = converter.convert(segment['text'])
        simplified_segments.append({'text': simplified_text, 'start': segment['start'], 'end': segment['end']})
    return simplified_segments


def preprocess_convert_aac_to_wav(folder_path, transcribed_files):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        file_name_without_ext = os.path.splitext(file)[0]

        # 检查文件是否已经转写，如果已转写，则跳过转换
        if file_name_without_ext in transcribed_files:
            print(f"{file} has already been transcribed. Skipping conversion.")
            continue

        if file.lower().endswith('.aac'):
            print(f"Converting {file} to WAV format.")
            convert_aac_to_wav(file_path)

# 转换 .aac 文件为 .wav
def convert_aac_to_wav(aac_file_path):
    wav_file_path = aac_file_path.replace('.aac', '.wav')
    command = ['ffmpeg', '-i', aac_file_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', wav_file_path]
    subprocess.run(command, check=True)
    # 如果要移除原本的.aac文件以减少空间占用，则去除注释符号。
    # os.remove(aac_file_path) 
    return wav_file_path

# 开始处理
process_audio_files(audio_folder, transcribed_files_log)
