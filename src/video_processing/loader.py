from moviepy import VideoFileClip


def load_video(file_path):
    return VideoFileClip(file_path)


def inspect_video(file_path):
    clip = VideoFileClip(file_path)

    try:
        info = {
            "filename": file_path,
            "duration_sec": round(clip.duration, 2),
            "fps": clip.fps,
            "resolution": clip.size,
        }

        print("\n VIDEO INFO ")
        for key, value in info.items():
            print(f"{key}: {value}")

    finally:
        clip.close()


def extract_audio_from_video(video_path, output_path):
    clip = VideoFileClip(video_path)

    try:
        audio = clip.audio
        audio.write_audiofile(output_path)
        print(f"Saved audio: {output_path}")

    finally:
        clip.close()