from video.frame_reader import read_video

video_path = "test_video.mp4"

result = read_video(video_path)

print("FPS:", result["fps"])
print("Duration:", result["duration"])
print("Frames extracted:", len(result["frames"]))
