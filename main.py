from ffmpeg import FFMPEG

# file = "https://v1.pinimg.com/videos/iht/hls/af/e6/a0/afe6a04e775f492fbb58b6fbf7e21eef.m3u8"
file = "sample.mp4"

ss = FFMPEG(input_stream=file)

# chapters = ss.metadata.get('chapters')
# print(chapters)
# ss.split(chapters)
# ss.remove_audio()
ss.take_screenshot(time="00:00:02")
# audio_stream = ss.audio_streams
# video_stream = ss.video_streams
# print(audio_stream)
# for stream in audio_stream:
#     if stream['name'] == "hin":
#         ss.extrac_audio(stream)

# ss.reverse_video(include_audio=False)
# ss.scale("480x240")
# ss.convert_to_gif()
