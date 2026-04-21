import os
from pydub import AudioSegment


def load_audio(file_path):
    return AudioSegment.from_file(file_path)


def trim_audio(audio, start_sec, end_sec):
    start_ms = start_sec * 1000
    end_ms = end_sec * 1000
    return audio[start_ms:end_ms]


def export_audio(audio, output_path, format=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if format is None:
        format = os.path.splitext(output_path)[1].replace(".", "").lower()

    audio.export(output_path, format=format)
    print(f"Saved: {output_path}")



def concatenate_audio(audio1, audio2):
    return audio1 + audio2

def change_volume(audio, db_change):
    return audio + db_change


def apply_fade(audio, fade_in_ms=2000, fade_out_ms=2000):
    return audio.fade_in(fade_in_ms).fade_out(fade_out_ms)    