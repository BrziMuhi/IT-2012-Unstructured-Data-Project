import os
from moviepy import VideoFileClip


def save_frame_at_time(video_path, output_path, t_seconds):
    clip = VideoFileClip(video_path)

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        clip.save_frame(output_path, t=t_seconds)
        print(f"Saved frame at {t_seconds}s -> {output_path}")
    finally:
        clip.close()


def extract_keyframes(video_path, output_folder, interval_seconds=5):
    clip = VideoFileClip(video_path)

    try:
        os.makedirs(output_folder, exist_ok=True)

        duration = int(clip.duration)
        for t in range(0, duration + 1, interval_seconds):
            output_path = os.path.join(output_folder, f"frame_{t}.png")
            clip.save_frame(output_path, t=t)
            print(f"Saved frame at {t}s -> {output_path}")

    finally:
        clip.close()