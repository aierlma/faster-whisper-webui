import os
import time
from auto_translation import run_whisper

def get_video_files(directory):
    """获取目录下所有视频文件"""
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm']
    video_files = []
    
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_files.append(os.path.join(directory, file))
    
    return video_files

def main():

    
    downloads_dir = r"D:\Downloads"
    print(f"开始扫描目录: {downloads_dir}")
    
    # 获取所有视频文件
    video_files = get_video_files(downloads_dir)
    
    if not video_files:
        print("未找到视频文件")
        return
    
    print(f"找到 {len(video_files)} 个视频文件")
    
    # 处理每个视频文件
    for i, video_file in enumerate(video_files, 1):
        print(f"\n处理第 {i}/{len(video_files)} 个文件: {video_file}")
        try:
            srt_path = run_whisper(video_file)
            print(f"成功处理文件: {video_file}")
            print(f"字幕文件保存在: {srt_path}")
        except Exception as e:
            print(f"处理文件 {video_file} 时出错: {str(e)}")
            continue

    print("\n所有文件处理完成!")

if __name__ == "__main__":
    main()
