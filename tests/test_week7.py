import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from src.storage.mongo import save_transcript_to_mongo
from src.audio_processing.loader import inspect_all_audio
from src.video_processing.frame_extractor import extract_keyframes
from src.video_processing.loader import (
    inspect_video,
    extract_audio_from_video,
)
from src.audio_processing.processor import (
    load_audio,
    trim_audio,
    export_audio,
    concatenate_audio,
    change_volume,
    apply_fade,
)
from src.audio_processing.transcriber import (
    transcribe_audio,
    save_transcript_json,
    save_transcript_txt,
    save_transcript_srt,
    chunked_transcribe,
)


def test_task1_inspect_audio():
    print("\nTASK 1: INSPECT AUDIO FILES ")
    logging.info("Task 1 started: inspect audio files")

    inspect_all_audio("data/raw/audio")

    logging.info("Task 1 completed")


def test_task2_trim_audio():
    print("\nTASK 2: TRIM AUDIO ")
    logging.info("Task 2 started: trim audio")

    input_file = "data/raw/audio/sample1.mp3"
    output_file = "data/processed/audio/sample1_trimmed.wav"

    audio = load_audio(input_file)
    trimmed = trim_audio(audio, 2, 8)
    export_audio(trimmed, output_file)

    logging.info("Task 2 completed: trimmed audio saved")


def test_task3_concatenate_audio():
    print("\nTASK 3: CONCATENATE AUDIO ")
    logging.info("Task 3 started: concatenate audio")

    file1 = "data/raw/audio/sample1.mp3"
    file2 = "data/raw/audio/sample1.wav"

    audio1 = load_audio(file1)
    audio2 = load_audio(file2)

    combined = concatenate_audio(audio1, audio2)

    output_file = "data/processed/audio/combined.wav"
    export_audio(combined, output_file)

    logging.info("Task 3 completed: combined audio saved")


def test_task4_volume_and_fade():
    print("\nTASK 4: VOLUME AND FADE")
    logging.info("Task 4 started: volume and fade")

    input_file = "data/raw/audio/sample1.mp3"

    audio = load_audio(input_file)

    louder_audio = change_volume(audio, 5)
    quieter_audio = change_volume(audio, -5)
    faded_audio = apply_fade(audio, fade_in_ms=2000, fade_out_ms=2000)

    export_audio(louder_audio, "data/processed/audio/sample1_louder.wav")
    export_audio(quieter_audio, "data/processed/audio/sample1_quieter.wav")
    export_audio(faded_audio, "data/processed/audio/sample1_faded.wav")

    logging.info("Task 4 completed: volume and fade files saved")


def test_task5_convert_audio():
    print("\nTASK 5: CONVERT AUDIO FORMAT")
    logging.info("Task 5 started: convert audio format")

    input_file = "data/raw/audio/sample1.mp3"

    audio = load_audio(input_file)

    output_file = "data/processed/audio/sample1_converted.flac"
    export_audio(audio, output_file)

    logging.info("Task 5 completed: converted audio saved")


def test_task6_video_processing():
    print("\nTASK 6: VIDEO PROCESSING")
    logging.info("Task 6 started: video processing")

    video_file = "data/raw/video/sample1.mp4"
    output_audio = "data/processed/audio/extracted_audio.mp3"

    inspect_video(video_file)
    extract_audio_from_video(video_file, output_audio)

    logging.info("Task 6 completed: video inspected and audio extracted")


def test_task7_extract_keyframes():
    print("\nTASK 7: EXTRACT KEYFRAMES")
    logging.info("Task 7 started: keyframe extraction")

    video_file = "data/raw/video/sample1.mp4"
    output_folder = "data/processed/frames"

    extract_keyframes(video_file, output_folder, interval_seconds=5)

    logging.info("Task 7 completed: keyframes extracted")


def test_task8_transcribe_short_audio():
    print("\nTASK 8: TRANSCRIBE SHORT AUDIO")
    logging.info("Task 8 started: short audio transcription")

    input_file = "data/raw/audio/sample1.mp3"

    transcript = transcribe_audio(input_file, model_size="base")

    print(f"Language: {transcript['language']}")
    print(f"Duration: {transcript['duration']} sec")
    print("\nSegments:")

    for segment in transcript["segments"]:
        print(f"[{segment['start']} - {segment['end']}] {segment['text']}")

    print("\nFull text preview:")
    print(transcript["full_text"][:300])

    save_transcript_json(transcript, "data/processed/transcripts/sample1.json")
    save_transcript_txt(transcript, "data/processed/transcripts/sample1.txt")
    save_transcript_srt(transcript, "data/processed/transcripts/sample1.srt")

    logging.info("Task 8 completed: short audio transcript saved")


def test_task9_transcribe_video_audio():
    print("\nTASK 9: TRANSCRIBE VIDEO AUDIO")
    logging.info("Task 9 started: transcribe extracted video audio")

    input_file = "data/processed/audio/extracted_audio.mp3"

    transcript = transcribe_audio(input_file, model_size="base")

    print(f"Language: {transcript['language']}")
    print(f"Duration: {transcript['duration']} sec")

    for segment in transcript["segments"]:
        print(f"[{segment['start']} - {segment['end']}] {segment['text']}")

    save_transcript_json(transcript, "data/processed/transcripts/video_audio.json")
    save_transcript_txt(transcript, "data/processed/transcripts/video_audio.txt")
    save_transcript_srt(transcript, "data/processed/transcripts/video_audio.srt")

    logging.info("Task 9 completed: video audio transcript saved")


def test_task10_chunked_transcription():
    print("\nTASK 10: CHUNKED TRANSCRIPTION")
    logging.info("Task 10 started: chunked transcription")

    input_file = "data/processed/audio/extracted_audio.mp3"
    output_folder = "data/processed/transcripts/chunked"

    transcript = chunked_transcribe(
        input_file,
        output_folder,
        chunk_length_ms=60000,
        model_size="base"
    )

    print(f"Language: {transcript['language']}")
    print(f"Duration: {transcript['duration']} sec")
    print(f"Total segments: {len(transcript['segments'])}")

    save_transcript_txt(transcript, "data/processed/transcripts/chunked_full.txt")
    save_transcript_srt(transcript, "data/processed/transcripts/chunked_full.srt")

    logging.info("Task 10 completed: chunked transcript saved")


def test_task11_store_transcript_mongo():
    print("\nTASK 11: STORE TRANSCRIPT IN MONGODB")
    logging.info("Task 11 started: save transcript to MongoDB")

    input_file = "data/raw/audio/sample1.mp3"

    transcript = transcribe_audio(input_file, model_size="base")

    save_transcript_to_mongo(
        transcript,
        source_path=input_file,
        model_name="base"
    )

    logging.info("Task 11 completed: transcript stored in MongoDB")


if __name__ == "__main__":
    test_task1_inspect_audio()
    test_task2_trim_audio()
    test_task3_concatenate_audio()
    test_task4_volume_and_fade()
    test_task5_convert_audio()
    test_task6_video_processing()
    test_task7_extract_keyframes()
    test_task8_transcribe_short_audio()
    test_task9_transcribe_video_audio()
    test_task10_chunked_transcription()
    test_task11_store_transcript_mongo()