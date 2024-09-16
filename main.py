from ffmpeg import FFMPEG

file = "sample.mp4"

ss = FFMPEG(file_path=file)

# chapters = ss.metadata.get('chapters')
# print(ss.metadata)
# ss.split(chapters)
# ss.remove_audio(output_file="sample_out_with_no_audio.mp4")
# ss.take_screenshot(time="00:00:12")
audio_stream = ss.audio_streams
video_stream = ss.video_streams
# print(audio_stream)
# for stream in audio_stream:
#     if stream['name'] == "eng":
#         ss.extrac_audio(stream)

ss.reverse_video(include_audio=False)
ss.scale("480x240")
