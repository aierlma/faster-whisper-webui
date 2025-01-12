import os
import subprocess
import sys

import json5

def load_whisper_config():
    """加载Whisper配置文件"""
    config_path = os.path.join("./", "config.json5")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json5.loads(f.read())
    return config

def convert_to_wav(input_file):
    """将视频文件转换为WAV格式"""
    print("正在将视频转换为音频...")
    wav_path = input_file + '.wav'
    
    # 使用ffmpeg进行转换
    cmd = [
        'ffmpeg.exe',
        '-y',              # 覆盖已存在的文件
        '-i', input_file,  # 输入文件
        '-acodec', 'pcm_s16le',  # 音频编码
        '-ac', '1',        # 单声道
        '-ar', '16000',    # 采样率
        wav_path
    ]
    
    process = subprocess.Popen(cmd)
    process.wait()
    print("音频转换完成")
    return wav_path

def run_whisper(input_file):
    """使用faster-whisper-webui生成字幕"""
    print("正在生成字幕...")
    config = load_whisper_config()
    output_dir = os.path.join(os.getcwd(), "./", config.get("output_dir", "output").strip("./"))
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 若同目录下已存在同文件名的wav后缀文件，则无需转换
    wav_path = os.path.join(output_dir, input_file + ".wav")

    if os.path.exists(wav_path):
        input_file = wav_path
    else:
        # 检查是否需要转换为WAV
        file_ext = os.path.splitext(input_file)[1].lower()
        if file_ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm']:
            input_file = convert_to_wav(input_file)
    
    # # 检查是否需要转换为WAV
    # file_ext = os.path.splitext(input_file)[1].lower()
    # if file_ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm']:
    #     input_file = convert_to_wav(input_file)
    
    # 构建基本命令，其余设置请在json5配置文件中指定
    whisper_dir = os.getcwd()
    cmd = [
        "python",
        os.path.join(whisper_dir, "cli.py")
    ] # Configuration options that will be used if they are not specified in the command line arguments.

    
    # 添加输入文件
    cmd.append(input_file)
    
    # 设置工作目录
    print("执行命令:", " ".join(cmd))
    subprocess.run(cmd, cwd=whisper_dir)
    print("字幕生成完成")
    
    # 获取生成的srt文件路径
    srt_filename = os.path.basename(input_file) + "-subs.srt"
    srt_path = os.path.join(output_dir, srt_filename)
    
    # # 如果生成了临时WAV文件，删除它
    # if input_file.endswith('.wav'):
    #     os.remove(input_file)
    
    if not os.path.exists(srt_path):
        raise FileNotFoundError(f"字幕文件未生成: {srt_path}")
    else :
            # 如果生成了临时WAV文件，删除它
        if input_file.endswith('.wav'):
            os.remove(input_file)
    
    return srt_path



def main():
    if len(sys.argv) < 1:
        print("使用方法: python auto_translation.py <视频文件路径>")
        sys.exit(1)
    
    input_file = sys.argv[1]

    
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)


    srt_path = run_whisper(input_file)
    print(f"字幕文件已生成: {srt_path}")
    
    print(f"\n处理完成!")
    print(f"翻译后的字幕文件保存在: {srt_path}")
        



if __name__ == "__main__":
    main()