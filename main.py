from ffmpeg import FFMPEG

# file = "https://v1.pinimg.com/videos/mc/hls/8f/b1/d6/8fb1d693ed2890d1eb45fef1127f3fd0.m3u8"
file = "sample.mp4"

app = FFMPEG(input_stream=file)
chapters = app.metadata.get('chapters')

if chapters:
    app.split(chapters)

app.remove_audio(force_replace=True)
app.take_screenshot(time="00:00:05", force_replace=True)
audio_stream = app.audio_streams
video_stream = app.video_streams

for stream in audio_stream:
    if stream['name'] == "eng":
        app.extrac_audio(stream, force_replace=True)
#
# ss.reverse_video(include_audio=False)
app.scale("720x480", force_replace=True)
app.convert_to_gif(force_replace=True)
