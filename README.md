# reddit-video-generator

Generate Reddit videos automatically using just one command

https://github.com/user-attachments/assets/6b07eb21-79c4-4c04-a786-2a75ee95aed3

## What is it?

An MVP for generating reddit videos automatically.

## Features

- [x] No API keys required
- [x] Supports multiple subreddits
- [x] Word-By-Word Timestamps
- [x] Easy to use

## Why does it exist?

I kept seeing these stupid videos on TikTok of Minecraft Parkour and a Text-To-Speech voice reading a Reddit post with the words in front. After seeing the number of views, I tried to make one, but it was taking too long. So I built this to automate the process. It's not the best, and I'm definitely not the first person to come up with this idea, but it does what I want it to do.

## How does it work?

I built it in Python mainly because of the [MoviePy](https://zulko.github.io/moviepy/) library, which is what I'm using for the videos. Here's the automated process:

1. Fetches a random post from a random subreddit. Uses .json trick instead of [PRAW](https://praw.readthedocs.io/en/stable/) to keep it free
2. Filters slurs
3. Text-to-Speech using [pyt2s](https://github.com/supersu-man/pyt2s)
4. Check if audio length is less than 60 seconds. If it is, restart the process.
5. Speech-To-Text using [whisperX](https://github.com/m-bain/whisperX). The reason why is to generate word-by-word timestamps
6. Download a random Minecraft parkour video off of [YouTube](https://www.youtube.com/) using [yt-dlp](https://github.com/yt-dlp/yt-dlp), and crop the dimensions using MoviePy
7. Generate MoviePy TextClips using timestamps from the Speech-To-Text
8. Combine everything together and export the final video via MoviePy

## Requirements

- Python 3.10 or higher

## How to install

1. Clone the repository
2. Create a virtual environment (optional but recommended)
```bash
# Windows
python -m venv env

# Linux/MacOS
python3 -m venv env
```
3. Activate the virtual environment. (if using one)
```bash
# Windows
.\env\Scripts\activate

# Linux/MacOS
source env/bin/activate
```
3. Run `pip install -r requirements.txt`
4. If you wish to contribute, you can make your changes

## How to run
```bash
# Windows
python main.py

# Linux/MacOS
python3 main.py
```

### Todo (in no particular order):

- [ ] Gender-based Text-To-Speech voice
- [ ] Replace Speech-To-Text text with filtered post text (to make it 100% accurate)
- [ ] Dockerize this
- [ ] Filter out NSFW posts
- [ ] Add more subreddits
- [ ] Add more customization options
- [ ] Maybe make an application using [PyQt](https://www.riverbankcomputing.com/software/pyqt/) or [Tkinter](https://wiki.python.org/moin/TkInter)
- [ ] Auto upload to TikTok and YouTube
