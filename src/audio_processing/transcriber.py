import os
import json
from pydub import AudioSegment
from faster_whisper import WhisperModel


def load_whisper_model(model_size="base"):
    model = WhisperModel(model_size, compute_type="int8")
    return model


def transcribe_audio(file_path, model_size="base"):
    model = load_whisper_model(model_size)

    segments, info = model.transcribe(file_path, word_timestamps=True)

    segment_list = []
    full_text = []

    for segment in segments:
        segment_data = {
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        }
        segment_list.append(segment_data)
        full_text.append(segment.text.strip())

    result = {
        "file_path": file_path,
        "language": info.language,
        "duration": round(info.duration, 2),
        "segments": segment_list,
        "full_text": " ".join(full_text)
    }

    return result


def save_transcript_json(transcript, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=4, ensure_ascii=False)

    print(f"Saved JSON: {output_path}")


def save_transcript_txt(transcript, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript["full_text"])

    print(f"Saved TXT: {output_path}")


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def save_transcript_srt(transcript, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcript["segments"], start=1):
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n")
            f.write(f"{segment['text']}\n\n")

    print(f"Saved SRT: {output_path}")


def chunked_transcribe(file_path, output_folder, chunk_length_ms=60000, model_size="base"):
    os.makedirs(output_folder, exist_ok=True)

    audio = AudioSegment.from_file(file_path)
    total_length = len(audio)

    model = load_whisper_model(model_size)

    all_segments = []
    full_text_parts = []
    detected_language = None

    chunk_index = 0
    start_ms = 0

    while start_ms < total_length:
        end_ms = min(start_ms + chunk_length_ms, total_length)

        chunk = audio[start_ms:end_ms]
        chunk_file = os.path.join(output_folder, f"chunk_{chunk_index}.wav")
        chunk_json = os.path.join(output_folder, f"chunk_{chunk_index}.json")

        if os.path.exists(chunk_json):
            print(f"Skipping chunk {chunk_index}, already processed.")
            with open(chunk_json, "r", encoding="utf-8") as f:
                chunk_result = json.load(f)
        else:
            chunk.export(chunk_file, format="wav")
            print(f"Processing chunk {chunk_index}: {start_ms/1000:.2f}s - {end_ms/1000:.2f}s")

            segments, info = model.transcribe(chunk_file, word_timestamps=True)

            if detected_language is None:
                detected_language = info.language

            chunk_segments = []
            chunk_text_parts = []

            for segment in segments:
                adjusted_start = round(segment.start + (start_ms / 1000), 2)
                adjusted_end = round(segment.end + (start_ms / 1000), 2)

                seg_data = {
                    "start": adjusted_start,
                    "end": adjusted_end,
                    "text": segment.text.strip()
                }
                chunk_segments.append(seg_data)
                chunk_text_parts.append(segment.text.strip())

            chunk_result = {
                "chunk_index": chunk_index,
                "source_file": file_path,
                "chunk_start_sec": round(start_ms / 1000, 2),
                "chunk_end_sec": round(end_ms / 1000, 2),
                "language": info.language,
                "segments": chunk_segments,
                "full_text": " ".join(chunk_text_parts)
            }

            with open(chunk_json, "w", encoding="utf-8") as f:
                json.dump(chunk_result, f, indent=4, ensure_ascii=False)

            print(f"Saved chunk transcript: {chunk_json}")

        all_segments.extend(chunk_result["segments"])
        full_text_parts.append(chunk_result["full_text"])

        chunk_index += 1
        start_ms += chunk_length_ms

    final_result = {
        "file_path": file_path,
        "language": detected_language,
        "duration": round(total_length / 1000, 2),
        "segments": all_segments,
        "full_text": " ".join(full_text_parts)
    }

    combined_json = os.path.join(output_folder, "combined_transcript.json")
    with open(combined_json, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=4, ensure_ascii=False)

    print(f"Saved combined transcript: {combined_json}")

    return final_result