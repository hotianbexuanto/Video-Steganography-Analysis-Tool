import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def select_video_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择视频文件",
        filetypes=[
            ("视频文件", "*.mp4 *.avi *.mov *.mkv"),
            ("所有文件", "*.*")
        ]
    )
    return file_path

def select_output_directory():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    directory = filedialog.askdirectory(
        title="选择输出目录"
    )
    return directory

def create_video_from_frames(frame_dir, output_video_path, original_fps=30, audio_path=None):
    """将图片序列合并为视频，使用原视频帧率"""
    images = [f for f in sorted(os.listdir(frame_dir)) if f.endswith('.png')]
    if not images:
        return False
    
    # 读取第一帧获取尺寸
    first_frame = cv2.imread(os.path.join(frame_dir, images[0]))
    height, width = first_frame.shape[:2]
    
    # 创建临时视频文件路径
    temp_video_path = output_video_path + '.temp.mp4'
    
    # 创建视频写入器，使用原视频帧率
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video_path, fourcc, original_fps, (width, height))
    
    # 写入所有帧
    total_frames = len(images)
    for i, image in enumerate(images):
        frame = cv2.imread(os.path.join(frame_dir, image))
        out.write(frame)
        # 显示进度
        print(f"\r正在处理帧: {i+1}/{total_frames}", end="")
    
    out.release()
    print()  # 换行
    
    # 如果有音频，添加到视频中
    if audio_path and os.path.exists(audio_path):
        try:
            # 读取临时视频
            video = VideoFileClip(temp_video_path)
            # 读取音频
            audio = AudioFileClip(audio_path)
            
            # 确保音频长度与视频匹配
            if video.duration > audio.duration:
                # 如果视频比音频长，循环音频
                audio = audio.loop(duration=video.duration)
            else:
                # 如果音频比视频长，裁剪音频
                audio = audio.subclip(0, video.duration)
            
            # 合并视频和音频
            final_video = video.set_audio(audio)
            # 保存最终视频，保持原始帧率
            final_video.write_videofile(
                output_video_path,
                codec='libx264',
                audio_codec='aac',
                fps=original_fps,
                preset='medium',  # 编码预设，可选 ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
                threads=4  # 使用多线程加速处理
            )
            # 清理
            video.close()
            audio.close()
            final_video.close()
            # 删除临时文件
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
        except Exception as e:
            print(f"添加音频时出错: {str(e)}")
            # 如果添加音频失败，至少保留无声视频
            if os.path.exists(temp_video_path):
                os.rename(temp_video_path, output_video_path)
    else:
        # 如果没有音频，直接重命名临时文件
        os.rename(temp_video_path, output_video_path)
    
    return True

def create_color_videos(input_video_path, output_dir):
    # 检查输入文件是否存在
    if not input_video_path or not os.path.exists(input_video_path):
        messagebox.showerror("错误", "请选择有效的视频文件！")
        return
    
    # 检查输出目录
    if not output_dir:
        messagebox.showerror("错误", "请选择输出目录！")
        return
        
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # 提取音频
        print("正在提取音频...")
        audio_path = os.path.join(output_dir, 'audio.mp3')
        try:
            video = VideoFileClip(input_video_path)
            original_fps = video.fps  # 获取原始视频的帧率
            if video.audio is not None:
                video.audio.write_audiofile(audio_path)
            video.close()
        except Exception as e:
            print(f"提取音频时出错: {str(e)}")
            audio_path = None
            original_fps = None
        
        # 读取视频
        cap = cv2.VideoCapture(input_video_path)
        
        if not cap.isOpened():
            messagebox.showerror("错误", "无法打开视频文件！")
            return
        
        # 获取视频属性
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if original_fps is None:
            original_fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # 创建所有需要的目录
        frames_dir = os.path.join(output_dir, 'frames')
        directories = {
            'basic': ['blue', 'green', 'red', 'grayscale'],
            'saturation': ['low_sat', 'high_sat', 'normal_sat'],
            'bit_planes': [f'bit_plane_{i}' for i in range(8)],
            'stegsolve': ['red_plane', 'green_plane', 'blue_plane', 
                         'inverse_red', 'inverse_green', 'inverse_blue',
                         'rgb_0', 'rgb_1', 'rgb_2', 'rgb_3', 'rgb_4', 'rgb_5', 'rgb_6', 'rgb_7'],
            'steganography': {
                'xor_analysis': ['r_xor_g', 'g_xor_b', 'b_xor_r'],
                'channel_operations': ['r_plus_g', 'g_plus_b', 'b_plus_r', 
                                     'r_minus_g', 'g_minus_b', 'b_minus_r'],
                'alpha_planes': ['alpha_0', 'alpha_1', 'alpha_2', 'alpha_3'],
                'color_filters': ['red_filter', 'green_filter', 'blue_filter',
                                'yellow_filter', 'cyan_filter', 'magenta_filter']
            }
        }
        
        # 创建所有目录
        for category, subdirs in directories.items():
            if isinstance(subdirs, dict):
                for subcat, subsubdirs in subdirs.items():
                    for subdir in subsubdirs:
                        full_path = os.path.join(frames_dir, category, subcat, subdir)
                        if not os.path.exists(full_path):
                            os.makedirs(full_path)
            else:
                for subdir in subdirs:
                    full_path = os.path.join(frames_dir, category, subdir)
                    if not os.path.exists(full_path):
                        os.makedirs(full_path)
        
        def process_bit_plane(img, bit):
            # 提取特定位平面
            plane = np.bitwise_and(img, 2**bit)
            plane = plane * (255 // 2**bit)
            return plane
        
        def adjust_saturation(img, factor):
            # 调整饱和度
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            s = cv2.multiply(s, factor)
            s = np.clip(s, 0, 255)
            hsv = cv2.merge([h, s, v])
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed_frames = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_number = str(processed_frames).zfill(6)
            
            # 1. 基本颜色通道处理
            b, g, r = cv2.split(frame)
            blue_frame = cv2.merge([b, np.zeros_like(b), np.zeros_like(b)])
            green_frame = cv2.merge([np.zeros_like(g), g, np.zeros_like(g)])
            red_frame = cv2.merge([np.zeros_like(r), np.zeros_like(r), r])
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 保存基本颜色通道
            cv2.imwrite(os.path.join(frames_dir, 'basic/blue', f'frame_{frame_number}.png'), blue_frame)
            cv2.imwrite(os.path.join(frames_dir, 'basic/green', f'frame_{frame_number}.png'), green_frame)
            cv2.imwrite(os.path.join(frames_dir, 'basic/red', f'frame_{frame_number}.png'), red_frame)
            cv2.imwrite(os.path.join(frames_dir, 'basic/grayscale', f'frame_{frame_number}.png'), gray_frame)
            
            # 2. 饱和度处理
            low_sat = adjust_saturation(frame, 0.5)  # 降低饱和度
            high_sat = adjust_saturation(frame, 1.5)  # 提高饱和度
            
            cv2.imwrite(os.path.join(frames_dir, 'saturation/low_sat', f'frame_{frame_number}.png'), low_sat)
            cv2.imwrite(os.path.join(frames_dir, 'saturation/high_sat', f'frame_{frame_number}.png'), high_sat)
            cv2.imwrite(os.path.join(frames_dir, 'saturation/normal_sat', f'frame_{frame_number}.png'), frame)
            
            # 3. 位平面处理
            for bit in range(8):
                bit_plane = process_bit_plane(frame, bit)
                cv2.imwrite(os.path.join(frames_dir, 'bit_planes', f'bit_plane_{bit}', f'frame_{frame_number}.png'), bit_plane)
            
            # 4. Stegsolve样式处理
            # 颜色通道反转
            inv_b = 255 - b
            inv_g = 255 - g
            inv_r = 255 - r
            
            # 保存Stegsolve样式结果
            steg_dir = os.path.join(frames_dir, 'stegsolve')
            cv2.imwrite(os.path.join(steg_dir, 'red_plane', f'frame_{frame_number}.png'), r)
            cv2.imwrite(os.path.join(steg_dir, 'green_plane', f'frame_{frame_number}.png'), g)
            cv2.imwrite(os.path.join(steg_dir, 'blue_plane', f'frame_{frame_number}.png'), b)
            cv2.imwrite(os.path.join(steg_dir, 'inverse_red', f'frame_{frame_number}.png'), inv_r)
            cv2.imwrite(os.path.join(steg_dir, 'inverse_green', f'frame_{frame_number}.png'), inv_g)
            cv2.imwrite(os.path.join(steg_dir, 'inverse_blue', f'frame_{frame_number}.png'), inv_b)
            
            # RGB位平面组合
            for bit in range(8):
                rgb_bit = cv2.merge([
                    process_bit_plane(b, bit),
                    process_bit_plane(g, bit),
                    process_bit_plane(r, bit)
                ])
                cv2.imwrite(os.path.join(steg_dir, f'rgb_{bit}', f'frame_{frame_number}.png'), rgb_bit)
            
            # 新增隐写分析处理
            steg_base_dir = os.path.join(frames_dir, 'steganography')
            
            # XOR 分析
            xor_dir = os.path.join(steg_base_dir, 'xor_analysis')
            r_xor_g = cv2.bitwise_xor(r, g)
            g_xor_b = cv2.bitwise_xor(g, b)
            b_xor_r = cv2.bitwise_xor(b, r)
            
            cv2.imwrite(os.path.join(xor_dir, 'r_xor_g', f'frame_{frame_number}.png'), r_xor_g)
            cv2.imwrite(os.path.join(xor_dir, 'g_xor_b', f'frame_{frame_number}.png'), g_xor_b)
            cv2.imwrite(os.path.join(xor_dir, 'b_xor_r', f'frame_{frame_number}.png'), b_xor_r)
            
            # 通道运算
            ops_dir = os.path.join(steg_base_dir, 'channel_operations')
            r_plus_g = cv2.add(r, g)
            g_plus_b = cv2.add(g, b)
            b_plus_r = cv2.add(b, r)
            r_minus_g = cv2.subtract(r, g)
            g_minus_b = cv2.subtract(g, b)
            b_minus_r = cv2.subtract(b, r)
            
            cv2.imwrite(os.path.join(ops_dir, 'r_plus_g', f'frame_{frame_number}.png'), r_plus_g)
            cv2.imwrite(os.path.join(ops_dir, 'g_plus_b', f'frame_{frame_number}.png'), g_plus_b)
            cv2.imwrite(os.path.join(ops_dir, 'b_plus_r', f'frame_{frame_number}.png'), b_plus_r)
            cv2.imwrite(os.path.join(ops_dir, 'r_minus_g', f'frame_{frame_number}.png'), r_minus_g)
            cv2.imwrite(os.path.join(ops_dir, 'g_minus_b', f'frame_{frame_number}.png'), g_minus_b)
            cv2.imwrite(os.path.join(ops_dir, 'b_minus_r', f'frame_{frame_number}.png'), b_minus_r)
            
            # 颜色滤镜
            filters_dir = os.path.join(steg_base_dir, 'color_filters')
            red_filter = cv2.multiply(frame, np.array([1.0, 0.0, 0.0]))
            green_filter = cv2.multiply(frame, np.array([0.0, 1.0, 0.0]))
            blue_filter = cv2.multiply(frame, np.array([0.0, 0.0, 1.0]))
            yellow_filter = cv2.multiply(frame, np.array([1.0, 1.0, 0.0]))
            cyan_filter = cv2.multiply(frame, np.array([0.0, 1.0, 1.0]))
            magenta_filter = cv2.multiply(frame, np.array([1.0, 0.0, 1.0]))
            
            cv2.imwrite(os.path.join(filters_dir, 'red_filter', f'frame_{frame_number}.png'), red_filter)
            cv2.imwrite(os.path.join(filters_dir, 'green_filter', f'frame_{frame_number}.png'), green_filter)
            cv2.imwrite(os.path.join(filters_dir, 'blue_filter', f'frame_{frame_number}.png'), blue_filter)
            cv2.imwrite(os.path.join(filters_dir, 'yellow_filter', f'frame_{frame_number}.png'), yellow_filter)
            cv2.imwrite(os.path.join(filters_dir, 'cyan_filter', f'frame_{frame_number}.png'), cyan_filter)
            cv2.imwrite(os.path.join(filters_dir, 'magenta_filter', f'frame_{frame_number}.png'), magenta_filter)
            
            # 更新进度
            processed_frames += 1
            progress = (processed_frames / total_frames) * 100
            print(f"\r处理进度: {progress:.1f}% (已处理 {processed_frames} 帧)", end="")
        
        # 释放资源
        cap.release()
        cv2.destroyAllWindows()
        
        # 将所有处理后的图片序列合并为视频
        print("\n正在生成视频文件...")
        videos_dir = os.path.join(output_dir, 'videos')
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
            
        # 遍历所有图片目录并生成对应的视频
        for root, dirs, files in os.walk(frames_dir):
            if files and any(f.endswith('.png') for f in files):
                # 构建相对路径作为视频文件名
                rel_path = os.path.relpath(root, frames_dir)
                video_name = f"{rel_path.replace(os.path.sep, '_')}.mp4"
                video_path = os.path.join(videos_dir, video_name)
                
                print(f"\n正在生成视频: {video_name}")
                if create_video_from_frames(root, video_path, original_fps, audio_path):
                    print(f"成功生成视频: {video_name}")
                else:
                    print(f"生成视频失败: {video_name}")
        
        # 清理音频文件
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        
        print("\n处理完成！")
        messagebox.showinfo("完成", "视频处理和合并完成！")
        
    except Exception as e:
        messagebox.showerror("错误", f"处理视频时出错：{str(e)}")

if __name__ == "__main__":
    # 选择输入视频文件
    input_video = select_video_file()
    if input_video:
        # 选择输出目录
        output_directory = select_output_directory()
        if output_directory:
            create_color_videos(input_video, output_directory) 