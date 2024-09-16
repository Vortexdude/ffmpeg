from ffmpeg import FFMPEG

file = "dms.mkv"

ss = FFMPEG(file_path=file)

# chapters = ss.metadata.get('chapters')
# print(chapters)
# ss.split(chapters)
# ss.remove_audio()
# ss.take_screenshot()
# audio_stream = ss.audio_streams
# video_stream = ss.video_streams
# print(audio_stream)
# for stream in audio_stream:
#     if stream['name'] == "hin":
#         ss.extrac_audio(stream)

# ss.reverse_video(include_audio=False)
ss.scale("480x240")
