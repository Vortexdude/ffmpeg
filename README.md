# FFmpeg Video Media Operations

This repository contains a Python module that leverages FFmpeg to perform various video media operations. The module is written in Python 3.12 and provides an easy-to-use interface for handling video files, extracting audio, taking screenshots, and more.

## Features

- **Split Video into Chapters**: Automatically splits a video file into chapters based on embedded metadata.
- **Remove Audio**: Strips the audio track from a video file.
- **Take Screenshots**: Captures screenshots from specific frames in the video.
- **Extract Audio**: Extracts audio tracks from a video file.
- **Stream Selection**: Allows selection of audio, video, or subtitle streams for further processing.

## Requirements

- Python 3.12
- FFmpeg installed and accessible via the command line

## Installation

1. Clone the repository:

   ```bash
   python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fffmpeg_vortexdude
   ```


## Usage
Here’s a simple example of how to use the module:
```python
from ffmpeg import FFMPEG

if __name__ == "__main__":
    INPUT_FILE = "dms.mkv"

    # Create a video processor instance and process the video
    video_processor = FFMPEG(input_file=INPUT_FILE)
    
    # Get chapters from the video
    chapters = video_processor.chapters
    
    # Split the video into chapters
    video_processor.split_chapter(chapters)
    
    # Remove the audio track from the video
    video_processor.remove_audio()
    
    # Take a screenshot from the video
    video_processor.take_screenshot()
    
    # Extract the audio track from the video
    video_processor.extract_audio()
    
    # Get the list of audio streams
    audio_streams = video_processor.streams(stream_selector='audio')
    
    # Get the list of video streams
    video_streams = video_processor.streams(stream_selector='video')
    
    # Get the list of subtitle streams
    subtitles = video_processor.streams(stream_selector='subtitle')
    
    # Example: Extract the English audio track
    for stream in audio_streams:
        if stream['tags'] == 'eng':
            video_processor.extract_audio()

```