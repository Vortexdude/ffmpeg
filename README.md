# FFmpeg Video Media Operations

This repository contains a Python module that leverages FFmpeg to perform various video media operations. The module is written in Python 3.12 and provides an easy-to-use interface for handling video files, extracting audio, taking screenshots, and more.

## Features
- **Splitting Chapters**: Split video by chapters metadata.
- **Take Screenshot**: Capture a screenshot at a specific timestamp.
- **Stream to MP4 Conversion**: Convert streaming files (e.g., .m3u8) to MP4.
- **View Metadata**: Access video and audio metadata, including chapters and streams.
- **Remove Audio from Video**: Remove audio tracks from the video file.
- **Convert Video to Audio**: Extract audio streams from a video and convert them to audio-only formats.

## Requirements

- Python 3.12
- FFmpeg installed and accessible via the command line

## Installation
To use this module, make sure you have Python 3.12 and FFmpeg installed.

   ```bash
   python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fffmpeg_vortexdude
   ```


## Usage
1. Initialize an FFMPEG Object
   ``` python
   from ffmpeg import FFMPEG
   
   file = "sample.mp4"
   ss = FFMPEG(input_stream=file)
   ```

2. Splitting Chapters <br> If the video contains chapters metadata, you can split the video into separate files for each chapter.
   ``` python
   from ffmpeg import FFMPEG
   
   file = "sample.mp4"
   ss = FFMPEG(input_stream=file)
   chapters = ss.metadata.get('chapters')
   ss.split(chapters)
   ```
3. Remove Audio from Video <br> Remove audio tracks from a video file:

   ``` python
   ss.remove_audio()
   ```
4. Take a screenshot <br> Capture a screenshot at a specific time in the video:

   ``` python
   ss.take_screenshot(time="00:00:05")
   ```
5. Convert Streaming Video to MP4 <br> You can convert a stream URL (e.g., .m3u8) to MP4:

    ``` python
    file = "https://v1.pinimg.com/videos/iht/hls/af/e6/a0/afe6a04e775f492fbb58b6fbf7e21eef.m3u8"
    ss = FFMPEG(input_stream=file)
    ss.convert_to_mp4(output="output.mp4")
    ```

6. Extract Audio Streams <br> Extract audio streams from a video:

    ``` python
    audio_stream = ss.audio_streams
    for stream in audio_stream:
        if stream['name'] == "hin":  # Example: Hindi audio track
            ss.extract_audio(stream)
    ```

7. Reverse Video <br> Reverse the video with or without audio:

    ``` python
    ss.reverse_video(include_audio=False)
    ```

8. Convert to GIF <br> Convert a portion of the video to a GIF:

    ``` python
    ss.convert_to_gif(start_time="00:00:10", duration=5)
    ```

9. Resize/Scale Video <br> Resize the video to specific dimensions:

    ``` python
    ss.scale("480x240")
    ```
