import librosa
import numpy as np
import os

os.system("rm -rf ./cache/*")
def get_audio_level_per_frame(audio_file, fps=30):
    y, sr = librosa.load(audio_file)
    frame_length = sr // fps
    # frame_length = int(frame_length)
    
    level_list = []

    for i in range(0, len(y), frame_length):
        if np.sum(abs(y[i:i+frame_length])) > 40:
            level_list.append("open.png")
        elif np.sum(abs(y[i:i+frame_length])) > 2:
            level_list.append("middle.png")
        else:
            level_list.append("close.png")
    level_list.append("close.png")
    second =  len(y) / sr
    return level_list, second
    

speech_path = 'test.wav'
level_list, second = get_audio_level_per_frame(speech_path)
print(len(level_list))
for idx, i in enumerate(level_list):
    os.system(f"cp ./src/{i} ./cache/{str(idx).rjust(4, '0')}.png")

# from glob import glob
# images = sorted(glob("./cache/*.png"))
# image_list = list()
# from PIL import Image
# for image_name in images:
#     image = Image.open(image_name)
#     image_list.append(image)

# duration = (1/30)*1000
# image_list[0].save("temp.gif",
#                     save_all=True,
#                     append_images=image_list[1:],
#                     duration=duration)

# from moviepy import editor

# video = editor.VideoFileClip( "temp.gif")
# audio = editor.AudioFileClip(speech_path)
# final_video = video.set_audio(audio)
# final_video.write_videofile("./result.mp4", fps=30, audio_fps=22050, codec = 'pcm_s32le')


os.system(f"ffmpeg -framerate 30 -pattern_type glob -i './cache/*.png' -i {speech_path} -map 0:v -map 1:a -c:v copy -shortest -c:v libx264 -pix_fmt yuv420p result.mp4")