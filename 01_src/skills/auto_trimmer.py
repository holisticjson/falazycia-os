import subprocess
import re
from pathlib import Path

def auto_trim_silence(input_path, output_name, noise_threshold=-30, min_silence_duration=0.5):
    ffmpeg_bin = r"C:\Users\tomas_yq1b9su\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
    
    input_path = Path(input_path)
    output_path = input_path.parent / output_name
    
    print(f"Analyzing silence in {input_path.name}...")
    
    # Detect silence
    cmd_detect = [
        ffmpeg_bin, "-i", str(input_path),
        "-af", f"silencedetect=noise={noise_threshold}dB:d={min_silence_duration}",
        "-f", "null", "-"
    ]
    
    result = subprocess.run(cmd_detect, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    output = result.stderr
    
    silence_starts = re.findall(r"silence_start: ([\d\.]+)", output)
    silence_ends = re.findall(r"silence_end: ([\d\.]+) \| silence_duration:", output)
    
    if not silence_starts:
        return str(input_path)
    
    keep_parts = []
    last_end = 0.0
    for start, end in zip(silence_starts, silence_ends):
        start = float(start)
        if start > last_end:
            keep_parts.append((last_end, start))
        last_end = float(end)
    
    # Get total duration
    cmd_duration = [ffmpeg_bin, "-i", str(input_path)]
    dur_res = subprocess.run(cmd_duration, stderr=subprocess.PIPE, text=True)
    dur_match = re.search(r"Duration: (\d+):(\d+):([\d\.]+)", dur_res.stderr)
    if dur_match:
        h, m, s = dur_match.groups()
        total_duration = float(h)*3600 + float(m)*60 + float(s)
        if last_end < total_duration:
            keep_parts.append((last_end, total_duration))

    # Build filter complex with CROSSFADES
    audio_filters = []
    fade_dur = 0.01 # 10ms crossfade to eliminate pops
    
    for i, (start, end) in enumerate(keep_parts):
        # Trim audio and apply tiny fades at edges
        seg_dur = end - start
        audio_filters.append(
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
            f"afade=t=in:ss=0:d={fade_dur},afade=t=out:st={seg_dur-fade_dur}:d={fade_dur}[a{i}];"
        )
    
    concat_a = "".join([f"[a{i}]" for i in range(len(keep_parts))])
    filter_complex = "".join(audio_filters) + f"{concat_a}concat=n={len(keep_parts)}:v=0:a=1[outa]"
    
    print(f"Removing {len(silence_starts)} silent periods with crossfades...")
    
    cmd_final = [
        ffmpeg_bin, "-y", "-i", str(input_path),
        "-filter_complex", filter_complex,
        "-map", "[outa]", str(output_path)
    ]
        
    subprocess.run(cmd_final, check=True)
    return str(output_path)

if __name__ == "__main__":
    sample = r"c:\Aplikacje MVP\Holistic Jason\04-ghost\nuggets\nugget_1_apel.mp3"
    result = auto_trim_silence(sample, "nugget_1_tight_pro.mp3")
    print(f"Pro Cleaned audio saved at: {result}")
