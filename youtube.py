from os import remove
from moviepy import AudioFileClip, VideoFileClip
from typing import Final
from random import choice, uniform
from yt_dlp import YoutubeDL
from tempfile import gettempdir
from os.path import join
from internet import UserAgents

parkourVideos: Final = [
    "https://www.youtube.com/watch?v=s600FYgI5-s",
    "https://www.youtube.com/watch?v=_H2cLn-OlIU",
]

def GetParkourVideo(audio: AudioFileClip) -> VideoFileClip:
    tempDir: Final = gettempdir()
    videoPath = None
    
    try:
        ydl_opts: Final = {
            "format": "bestvideo[ext=mp4]/best[ext=mp4]/mp4/best",
            "outtmpl": f"{tempDir}/%(id)s.%(ext)s",
            "noplaylist": True,
            "quiet": True,
            "merge_output_format": "mp4",
            "user-agent": choice(UserAgents)
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(choice(parkourVideos), download=True)
        
        videoPath = join(tempDir, f"{info['id']}.{info['ext']}")
        
        video: Final = VideoFileClip(videoPath)
        
        # Create the clipped version
        startTime: Final = uniform(0, max(0, video.duration - audio.duration))
        clippedVideo: Final[VideoFileClip] = video.subclipped(startTime, startTime + audio.duration)
        
        target_width: Final = 1080
        target_height: Final = 1920
        
        crop_width: Final = min(target_width, clippedVideo.w)
        crop_height: Final = min(target_height, clippedVideo.h)
        
        croppedVideo: Final[VideoFileClip] = clippedVideo.cropped(
            x1=max(0, (clippedVideo.w - crop_width) // 2),
            y1=max(0, (clippedVideo.h - crop_height) // 2), 
            width=crop_width,
            height=crop_height
        )
        finalVideo: Final[VideoFileClip] = croppedVideo.with_audio(audio)
        
        return finalVideo
        
    finally:
        # Clean up the downloaded file
        if videoPath:
            try:
                remove(videoPath)
            except PermissionError:
                # If still can't delete, it will be cleaned up later by the OS
                print(f"Warning: Could not delete temporary file {videoPath}")
                pass