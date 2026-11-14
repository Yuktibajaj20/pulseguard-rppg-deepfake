
from pipeline import analyze_video
import json

result = analyze_video("test_video.mp4")

print(json.dumps(result, indent=4))

