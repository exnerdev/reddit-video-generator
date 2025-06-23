#!/usr/bin/env python
from os import fsync, remove
from os.path import exists, splitext, join
from tempfile import NamedTemporaryFile, gettempdir
from typing import Final
from moviepy import AudioFileClip, CompositeVideoClip, TextClip
from filterText import FilterText
from reddit import GetRedditPost
from speechToText import SpeechToText
from textToSpeech import TextToSpeech
from youtube import GetParkourVideo
from sys import version_info, exit, argv
from platform import system
from time import sleep

def main(videoName: str) -> None:
    tempAudioPath = None
    audio = None
    video = None
    
    try:
        print("[Step 1] Fetching Reddit post...")
        redditPost: Final = GetRedditPost()
        postTitle: Final = FilterText(redditPost["title"])
        postContent: Final = FilterText(redditPost["selftext"])

        print("[Step 2] Transcribing Reddit post...")
        audioData: Final = TextToSpeech(postTitle + "\n\n" + postContent)

        if not audioData or len(audioData) == 0:
            raise ValueError("No audio data received from TextToSpeech")
        
        if len(audioData) < 1024:  # less than 1KB, likely invalid
            print(f"Audio data too small (size: {len(audioData)} bytes). Retrying...")
            return main(videoName)
        
        with NamedTemporaryFile(delete=False, suffix=".mp3", mode='wb') as temp_audio:
            temp_audio.write(audioData)
            temp_audio.flush()
            fsync(temp_audio.fileno())
            tempAudioPath = temp_audio.name
        
        if not exists(tempAudioPath):
            raise FileNotFoundError(f"Temporary audio file was not created: {tempAudioPath}")
        
        sleep(0.1)
        
        print("[Step 3] Validating Audio Length...")
        try:
            audio = AudioFileClip(tempAudioPath)
        except Exception as e:
            print(f"Failed to load audio file. File size: {exists(tempAudioPath) and 'exists' or 'missing'}")
            if exists(tempAudioPath):
                import os
                print(f"File size: {os.path.getsize(tempAudioPath)} bytes")
            raise e
        if audio.duration < 60.0:
            print("Audio duration is too short. Retrying")
            audio.close()
            remove(tempAudioPath) if exists(tempAudioPath) else None
            return main(videoName)

        print("[Step 4] Generating Timestamps...")
        timestamps: Final = SpeechToText(tempAudioPath)

        print("[Step 5] Downloading Parkour Video...")
        video = GetParkourVideo(audio)

        print("[Step 6] Adding Timestamps to Video...")
        text_clips = []
        prev_end = 0.0
        for segment in timestamps:
            for word in segment["words"]:
                # Todo - Replace word with one in post text to make it accurate
                start = prev_end
                end = word["end"]
                txt_clip = (
                    TextClip(
                        text=word["word"],
                        font="./NotoSans-Bold.ttf",
                        font_size=70,
                        color="white",
                        stroke_color="black",
                        stroke_width=6, 
                        size=video.size,
                        method="caption",
                    )
                    .with_position(("center", "center"))
                    .with_start(start)
                    .with_end(end)
                )
                text_clips.append(txt_clip)
                prev_end = end
        
        final_video = CompositeVideoClip([video, *text_clips])
        
        print("[Step 7] Writing final video...")
        final_video.write_videofile(f"{videoName}.mp4", fps=60, codec="libx264", temp_audiofile=join(gettempdir(), f"{redditPost['id']}.aac"), audio_codec="aac")
        
        print("✅ Video creation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        # Clean up resources
        if audio:
            try:
                audio.close()
            except:
                pass  # Ignore errors when closing
        if video:
            try:
                video.close()
            except:
                pass  # Ignore errors when closing
        if tempAudioPath and exists(tempAudioPath):
            try:
                remove(tempAudioPath)
            except:
                pass  # Ignore errors when removing temp file

if __name__ == "__main__":
    if version_info.major < 3 or version_info.minor < 10:
        print("reddit-video-generator requires Python 3.10 or higher. Sorry :(")
        exit()
    if len(argv) < 2:
        if system() == "Windows":
            print("Usage: python main.py <VIDEONAME>")
        else:
            print("Usage: python3 main.py <VIDEONAME>")
        exit()
    if len(splitext(argv[1])) > 2:
        print("Please provide a video name without an extension")
        exit()
    
    main(argv[1])