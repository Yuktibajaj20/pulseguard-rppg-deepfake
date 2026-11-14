from pathlib import Path
import requests
import json

API_URL = "http://127.0.0.1:8000/analyze"
VIDEO_FOLDER = Path("test_videos")

VIDEO_FOLDER.mkdir(exist_ok=True)

videos = list(VIDEO_FOLDER.glob("*.mp4"))
videos += list(VIDEO_FOLDER.glob("*.mov"))
videos += list(VIDEO_FOLDER.glob("*.avi"))

if not videos:
    print("No videos found. Put test videos inside backend/test_videos/")
    raise SystemExit

for video_path in videos:
    print(f"\nTesting: {video_path.name}")

    try:
        with video_path.open("rb") as video:
            response = requests.post(
                API_URL,
                files={
                    "file": (
                        video_path.name,
                        video,
                        "video/mp4"
                    )
                },
                timeout=300
            )

        print("HTTP status:", response.status_code)

        try:
            result = response.json()
        except ValueError:
            print("Server returned non-JSON response:")
            print(response.text[:1000])
            continue

        if response.ok:
            print("Processing:", result.get("status"))
            print("Assessment:", result.get("assessment"))
            print("Heart rates:", result.get("heart_rates"))
            print("Signal quality:", result.get("signal_quality"))

            output_path = video_path.with_name(
                video_path.stem + "_result.json"
            )
            output_path.write_text(
                json.dumps(result, indent=4),
                encoding="utf-8"
            )
            print("Saved:", output_path.name)

        else:
            print("Error:", result)

    except requests.RequestException as error:
        print("Request failed:", error)