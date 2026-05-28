import json
from pathlib import Path
import subprocess
import textwrap

# Paths
root = Path(r"c:\Aplikacje MVP\Holistic Jason")
json_path = root / "04-ghost" / "nuggets" / "nugget_1_tight_subtitles.json"
ffmpeg_bin = r"C:\Users\tomas_yq1b9su\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
# Important: We need a video of the SAME length as the tight audio
# The faceless pipeline will automatically match audio duration if we run it again
# BUT for this test, I will just apply the tight audio to the existing video clips
input_video_raw = root / "generated_media" / "faceless" / "real_broll_0.mp4" # Just a starting point
output_video = root / "generated_media" / "faceless" / "HOLISTIC_JASON_TURBO_FINAL.mp4"
audio_tight = root / "04-ghost" / "nuggets" / "nugget_1_tight.mp3"

# Load JSON
with open(json_path, 'r', encoding='utf-8') as f:
    subs = json.load(f)

def time_to_sec(t_str):
    parts = t_str.split(':')
    return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])

def clean_text(t):
    replacements = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z', 'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'}
    for k, v in replacements.items(): t = t.replace(k, v)
    return t.upper().replace("'", "").replace(":", "")

# Build filters
filters = []
for s in subs:
    start, end = time_to_sec(s['start']), time_to_sec(s['end'])
    raw_text = clean_text(s['text'])
    lines = textwrap.wrap(raw_text, width=15)
    for i, line in enumerate(lines):
        line_offset = (i - (len(lines)-1)/2) * 55
        y_pos = f"h*0.75 + {line_offset}"
        f = (f"drawtext=text='{line}':fontcolor=0x00F0FF:fontsize=45:fontfile=bahnschrift.ttf:"
             f"x=(w-text_w)/2:y={y_pos}:box=1:boxcolor=black@0.6:boxborderw=10:"
             f"enable='between(t,{start},{end})'")
        filters.append(f)

filter_str = ','.join(filters)

# Step 1: Re-assemble video to match TIGHT audio length (12.6s)
# I'll use the faceless_pipeline logic directly here
from skills.faceless_pipeline import create_faceless_video
# We need about 3 clips of 4-5 seconds each
clips = [
    str(root / "generated_media/faceless/real_broll_0.mp4"),
    str(root / "generated_media/faceless/real_broll_1.mp4"),
    str(root / "generated_media/faceless/real_broll_2.mp4")
]

# Create the video skeleton with tight audio
print("Assembling video skeleton for TIGHT audio...")
video_skeleton = create_faceless_video(str(audio_tight), clips, "temp_tight_skeleton.mp4")

# Step 2: Burn subtitles onto the tight skeleton
print("Burning subtitles onto the TIGHT skeleton...")
cmd_burn = [
    ffmpeg_bin, "-y",
    "-i", video_skeleton,
    "-vf", filter_str,
    "-c:a", "copy",
    str(output_video)
]

subprocess.run(cmd_burn, check=True)
print(f"TURBO SUCCESS! Video saved at: {output_video}")
