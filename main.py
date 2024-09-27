from ffmpeg import FFMPEG

file = "sample.mp4"
# file = "audio.mp3"
watermark_file = "watermark.jpeg"
# file = "audio_modified.mp3"
# file = "tanjiro.jpeg"
# file = "https://v1.pinimg.com/videos/mc/hls/8f/b1/d6/8fb1d693ed2890d1eb45fef1127f3fd0.m3u8"

#TODO check the file type like its audio or video without using the extension and then fetch the metadata
#TODO Audio_processing for manipulate the metadata of the audio file

app = FFMPEG(input_stream=file)
# app.add_metadata(genre="hiphop", album="Encore", artist="Nitin")
# print(app.metadata.get('format').get('tags'))
# app.convert_to_gif(seek="00:00:10", force_replace=True)

# print(app.metadata)

# chapters = app.metadata.get('chapters')
#
# if chapters:
#     app.split(chapters)
#
# app.remove_audio(force_replace=True)
# app.take_screenshot(time="00:00:11")
# audio_stream = app.audio_streams
# video_stream = app.video_streams
#
# for stream in audio_stream:
#     if stream['name'] == "eng":
#         app.extrac_audio(stream, force_replace=True)
# #
# # ss.reverse_video(include_audio=False)
# app.scale("720x480", force_replace=True)
# app.convert_to_gif(force_replace=True, width=720)
# app.add_watermark(watermark_file, position="bottom_left", padding=20)
app.add_text(text="NenoSystems.com", position="bottom_left", font_size=30, start_after=10, duration=30)
# TODO validate the position if its a tuple then serves as the coordinate
# TODO VALIDATE THE arg types as well

