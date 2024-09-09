from ffmpeg import FFMPEG


if __name__ == "__main__":
    INPUT_FILE = "dms.mkv"

    # Create a video processor instance and process the video
    video_processor = FFMPEG(input_file=INPUT_FILE)
    video_processor.width = 720
    video_processor.height = 1080
    video_processor.scale()
    # chapters = video_processor.chapters
    # video_processor.split_chapter(chapters)
    # video_processor.remove_audio()
    # video_processor.take_screenshot()
    # video_processor.extrac_audio()
    # for stream in audio_streams:
    #     if stream['tags']['language'] == 'eng':
    #         video_processor.extrac_audio(stream)
    # video_processor.reverse_video()
    