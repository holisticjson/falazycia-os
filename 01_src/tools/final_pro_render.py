import json
from pathlib import Path
import subprocess
import textwrap
import sys

# Add root to sys path for imports
root = Path(r"c:\Aplikacje MVP\Holistic Jason")
sys.path.append(str(root))

from skills.faceless_pipeline import create_faceless_video

# Paths
json_path = root / "04-ghost" / "nuggets" / "nugget_1_tight_subtitles.json"
ffmpeg_bin = r"C:\Users\tomas_yq1b9su\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
audio_pro = root / "04-ghost" / "nuggets" / "nugget_1_tight_pro.mp3"
output_video = root / "generated_media" / "faceless" / "HOLISTIC_JASON_PRO_FINAL.mp4"
filter_script = root / "final_filter.txt"

# Load JSON
with open(json_path, 'r', encoding='utf-8') as f:
    subs = json.load(f)

def time_to_sec(t_str):
    parts = t_str.split(':')
    return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])

def clean_text(t):
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
        # Use local font file
        f_text = (f"drawtext=text='{line}':fontcolor=0x00F0FF:fontsize=45:fontfile=bahnschrift.ttf:"
                  f"x=(w-text_w)/2:y={y_pos}:box=1:boxcolor=black@0.6:boxborderw=10:"
                  f"enable='between(t,{start},{end})'")
        filters.append(f_text)

filter_str = ','.join(filters)

# Create skeleton
print("Creating video skeleton...")
clips = [
    str(root / "generated_media/faceless/real_broll_0.mp4"),
    str(root / "generated_media/faceless/real_broll_1.mp4"),
    str(root / "generated_media/faceless/real_broll_2.mp4")
]
video_skeleton = create_faceless_video(str(audio_pro), clips, "temp_pro_skeleton.mp4")

# Save filter script
with open(filter_script, 'w', encoding='utf-8') as f:
    f.write(filter_str)

# Burn subs
print("Burning subtitles...")
cmd_burn = [
    ffmpeg_bin, "-y",
    "-i", video_skeleton,
    "-filter_script:v", str(filter_script),
    "-c:a", "copy",
    str(output_video)
]

subprocess.run(cmd_burn, check=True)
print(f"PRO SUCCESS! Video saved at: {output_video}")
