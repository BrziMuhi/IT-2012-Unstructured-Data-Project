import os
from pydub import AudioSegment


def inspect_audio(file_path):
    audio = AudioSegment.from_file(file_path)

    info = {
        "filename": os.path.basename(file_path),
        "format": os.path.splitext(file_path)[1].replace(".", "").upper(),
        "duration_sec": round(len(audio) / 1000, 2),
        "channels": audio.channels,
        "channel_type": "Stereo" if audio.channels == 2 else "Mono",
        "frame_rate_hz": audio.frame_rate,
        "bit_depth": audio.sample_width * 8,
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2)
    }

    return info


def inspect_all_audio(folder="data/raw/audio"):
    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return

    files = os.listdir(folder)
    if not files:
        print(f"No audio files found in {folder}")
        return

    for file_name in files:
        file_path = os.path.join(folder, file_name)

        if not os.path.isfile(file_path):
            continue

        try:
            info = inspect_audio(file_path)

            print("\nAUDIO INFO ")
            for key, value in info.items():
                print(f"{key}: {value}")

        except Exception as e:
            print(f"Error loading {file_name}: {e}")