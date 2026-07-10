import os
import json
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

def trim_video(args: Dict[str, Any], **kwargs) -> str:
    """
    Trim a video to the specified start and end times.
    """
    input_path = args.get("input_path")
    output_path = args.get("output_path")
    start_time = args.get("start_time")
    end_time = args.get("end_time")
    
    if not all([input_path, output_path, start_time is not None, end_time is not None]):
        return "Error: Missing one or more required arguments (input_path, output_path, start_time, end_time)."

    try:
        start_time = float(start_time)
        end_time = float(end_time)
    except ValueError:
        return "Error: start_time and end_time must be numbers."

    try:
        from moviepy.editor import VideoFileClip
        local_input_path = "/tmp/dl_input.mp4"
        if input_path.startswith("gs://"):
            os.system(f"gsutil cp {input_path} {local_input_path}")
            input_path = local_input_path
        elif input_path.startswith("http://") or input_path.startswith("https://"):
            import urllib.request
            try:
                urllib.request.urlretrieve(input_path, local_input_path)
                input_path = local_input_path
            except Exception as e:
                return f"Error downloading input video: {e}"

        with VideoFileClip(input_path) as clip:
            trimmed = clip.subclip(start_time, end_time)
            trimmed.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return f"Video trimmed successfully and saved to {output_path}"
    except ImportError:
        return "Error: moviepy is not installed."
    except Exception as e:
        return f"Failed to trim video: {str(e)}"

def format_for_reels(args: Dict[str, Any], **kwargs) -> str:
    """
    Crop or resize video to 9:16 vertical format (1080x1920).
    """
    input_path = args.get("input_path")
    output_path = args.get("output_path")
    
    if not all([input_path, output_path]):
        return "Error: Missing input_path or output_path."

    try:
        from moviepy.editor import VideoFileClip
        import moviepy.video.fx.all as vfx

        local_input_path = "/tmp/dl_format_input.mp4"
        if input_path.startswith("gs://"):
            os.system(f"gsutil cp {input_path} {local_input_path}")
            input_path = local_input_path
        elif input_path.startswith("http://") or input_path.startswith("https://"):
            import urllib.request
            try:
                urllib.request.urlretrieve(input_path, local_input_path)
                input_path = local_input_path
            except Exception as e:
                return f"Error downloading input video for formatting: {e}"

        with VideoFileClip(input_path) as clip:
            w, h = clip.size
            target_ratio = 9/16
            current_ratio = w/h
            if current_ratio > target_ratio:
                new_w = int(h * target_ratio)
                x_center = w / 2
                cropped = clip.crop(x1=x_center - new_w/2, y1=0, x2=x_center + new_w/2, y2=h)
            else:
                new_h = int(w / target_ratio)
                y_center = h / 2
                cropped = clip.crop(x1=0, y1=y_center - new_h/2, x2=w, y2=y_center + new_h/2)
                
            resized = cropped.resize(height=1920, width=1080)
            resized.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return f"Video formatted for reels (9:16) and saved to {output_path}"
    except Exception as e:
        return f"Failed to format video: {str(e)}"

def search_pixabay_broll(args: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
    """
    Search Pixabay for free stock videos (b-roll).
    """
    query = args.get("query")
    
    if not query:
        return [{"error": "Missing search query."}]

    import requests
    import urllib.parse
    api_key = os.getenv("PIXABAY_API_KEY")
    if not api_key:
        return [{"error": "PIXABAY_API_KEY is not set."}]
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://pixabay.com/api/videos/?key={api_key}&q={encoded_query}&video_type=all&per_page=5"
    
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for v in data.get("hits", []):
            videos = v.get("videos", {})
            video_obj = videos.get("medium") or videos.get("large") or videos.get("small") or videos.get("tiny")
            if video_obj and video_obj.get("url"):
                results.append({
                    "id": v["id"],
                    "url": video_obj["url"],
                    "duration": v.get("duration", 0)
                })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def add_subtitles(args: Dict[str, Any], **kwargs) -> str:
    """
    Add subtitles to a video using an SRT file.
    """
    input_path = args.get("input_path")
    srt_path = args.get("srt_path")
    output_path = args.get("output_path")
    
    if not all([input_path, srt_path, output_path]):
        return "Error: Missing one or more required arguments (input_path, srt_path, output_path)."

    try:
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        from moviepy.video.tools.subtitles import SubtitlesClip
        
        local_input_path = "/tmp/dl_sub_input.mp4"
        if input_path.startswith("gs://"):
            os.system(f"gsutil cp {input_path} {local_input_path}")
            input_path = local_input_path
        elif input_path.startswith("http://") or input_path.startswith("https://"):
            import urllib.request
            try:
                urllib.request.urlretrieve(input_path, local_input_path)
                input_path = local_input_path
            except Exception as e:
                return f"Error downloading input video for subtitles: {e}"

        local_srt_path = "/tmp/dl_sub.srt"
        if srt_path.startswith("gs://"):
            os.system(f"gsutil cp {srt_path} {local_srt_path}")
            srt_path = local_srt_path
        elif srt_path.startswith("http://") or srt_path.startswith("https://"):
            import urllib.request
            try:
                urllib.request.urlretrieve(srt_path, local_srt_path)
                srt_path = local_srt_path
            except Exception as e:
                return f"Error downloading SRT file: {e}"

        brand_config_path = os.path.join(os.path.dirname(__file__), "brand_config.json")
        color = "white"
        font = "Arial"
        if os.path.exists(brand_config_path):
            with open(brand_config_path, "r") as f:
                config = json.load(f)
                color = config.get("primary_color", "white")
                font = config.get("font_family", "Arial")
                
        generator = lambda txt: TextClip(txt, font=font, fontsize=50, color=color, stroke_color="black", stroke_width=2)
        subs = SubtitlesClip(srt_path, generator)
        
        with VideoFileClip(input_path) as video:
            result = CompositeVideoClip([video, subs.set_pos(('center', 'bottom'))])
            result.write_videofile(output_path, fps=video.fps, codec="libx264", audio_codec="aac")
            
        return f"Subtitles added successfully to {output_path}"
    except Exception as e:
        return f"Failed to add subtitles: {str(e)}"

def generate_gcp_tts(args: Dict[str, Any], **kwargs) -> str:
    """
    Generate Text-to-Speech using Google Cloud TTS.
    """
    text = args.get("text")
    output_path = args.get("output_path")
    voice_name = args.get("voice_name", "pl-PL-Standard-B")
    
    if not all([text, output_path]):
        return "Error: Missing text or output_path."

    try:
        from google.cloud import texttospeech
        
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="pl-PL",
            name=voice_name
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            
        return f"Audio generated and saved to {output_path}"
    except ImportError:
        return "Error: google-cloud-texttospeech is not installed."
    except Exception as e:
        return f"Failed to generate TTS: {str(e)}"

def assemble_reel_moviepy(args: Dict[str, Any], **kwargs) -> str:
    """
    Assemble multiple video clips and an audio track into a single reel.
    """
    video_paths = args.get("video_paths")
    audio_path = args.get("audio_path")
    output_path = args.get("output_path")
    
    if not audio_path:
        return "Error: audio_path is missing or None. Please provide the TTS audio path."

    if not output_path:
        return "Error: output_path is missing or None."

    if not video_paths:
        # Fallback to video_urls if provided in kwargs
        video_paths = kwargs.get("video_urls", [])
        if not video_paths:
            return "Error: video_paths is missing or empty."

    if isinstance(video_paths, str):
        video_paths = [video_paths]

    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
        import math

        local_audio = "/tmp/dl_audio.mp3"
        if audio_path.startswith("gs://"):
            os.system(f"gsutil cp {audio_path} {local_audio}")
            audio_path = local_audio
        elif audio_path.startswith("http://") or audio_path.startswith("https://"):
            import urllib.request
            try:
                urllib.request.urlretrieve(audio_path, local_audio)
                audio_path = local_audio
            except Exception as e:
                return f"Error downloading audio: {e}"

        audio = AudioFileClip(audio_path)
        target_duration = audio.duration
        
        clips = []
        local_video_paths = []
        for i, p in enumerate(video_paths):
            local_p = f"/tmp/dl_video_{i}.mp4"
            if p.startswith("gs://"):
                os.system(f"gsutil cp {p} {local_p}")
                local_video_paths.append(local_p)
            elif p.startswith("http://") or p.startswith("https://"):
                import urllib.request
                try:
                    urllib.request.urlretrieve(p, local_p)
                    local_video_paths.append(local_p)
                except Exception as e:
                    print(f"Failed to download {p}: {e}")
                    local_video_paths.append(p)
            else:
                local_video_paths.append(p)

        for path in local_video_paths:
            clips.append(VideoFileClip(path))
            
        if not clips:
            return "Error: No video paths provided after download/processing."
            
        formatted_clips = []
        for clip in clips:
            w, h = clip.size
            target_ratio = 9/16
            current_ratio = w/h
            if current_ratio > target_ratio:
                new_w = int(h * target_ratio)
                x_center = w / 2
                cropped = clip.crop(x1=x_center - new_w/2, y1=0, x2=x_center + new_w/2, y2=h)
            else:
                new_h = int(w / target_ratio)
                y_center = h / 2
                cropped = clip.crop(x1=0, y1=y_center - new_h/2, x2=w, y2=y_center + new_h/2)
            
            resized = cropped.resize(height=1920, width=1080)
            formatted_clips.append(resized)
            
        final_video = concatenate_videoclips(formatted_clips, method="compose")
        
        if final_video.duration < target_duration:
            loops_needed = math.ceil(target_duration / final_video.duration)
            final_video = concatenate_videoclips([final_video] * loops_needed, method="compose")
            
        final_video = final_video.subclip(0, target_duration)
        final_video = final_video.set_audio(audio)
        
        final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
        
        for c in clips:
            c.close()
        for fc in formatted_clips:
            fc.close()
        audio.close()
        final_video.close()
            
        return f"Reel assembled successfully and saved to {output_path}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Failed to assemble reel: {str(e)}"

def register_tools(ctx: Any) -> None:
    ctx.register_tool(
        name="video_editor_trim",
        toolset="video_editor",
        schema={
            "name": "video_editor_trim",
            "description": "Trim a video. Provide input_path, output_path, start_time (seconds), end_time (seconds).",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {"type": "string", "description": "Path to the input video file."},
                    "output_path": {"type": "string", "description": "Path to save the trimmed video."},
                    "start_time": {"type": "number", "description": "Start time in seconds."},
                    "end_time": {"type": "number", "description": "End time in seconds."},
                },
                "required": ["input_path", "output_path", "start_time", "end_time"]
            }
        },
        handler=trim_video,
    )
    ctx.register_tool(
        name="video_editor_format_reels",
        toolset="video_editor",
        schema={
            "name": "video_editor_format_reels",
            "description": "Crop and resize video to 9:16 vertical format (1080x1920) for reels/shorts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {"type": "string", "description": "Path to the input video file."},
                    "output_path": {"type": "string", "description": "Path to save the formatted video."},
                },
                "required": ["input_path", "output_path"]
            }
        },
        handler=format_for_reels,
    )
    ctx.register_tool(
        name="video_editor_search_broll",
        toolset="video_editor",
        schema={
            "name": "video_editor_search_broll",
            "description": "Search Pixabay for free stock videos. Provide query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query for b-roll footage."},
                    "orientation": {"type": "string", "description": "Video orientation ('portrait', 'landscape', 'square') - ignored by Pixabay but kept for compatibility.", "enum": ["portrait", "landscape", "square"], "default": "portrait"},
                },
                "required": ["query"]
            }
        },
        handler=search_pixabay_broll,
    )
    ctx.register_tool(
        name="video_editor_add_subtitles",
        toolset="video_editor",
        schema={
            "name": "video_editor_add_subtitles",
            "description": "Add subtitles to a video. Provide input_path, srt_path, output_path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {"type": "string", "description": "Path to the input video file."},
                    "srt_path": {"type": "string", "description": "Path to the SRT subtitle file."},
                    "output_path": {"type": "string", "description": "Path to save the video with subtitles."},
                },
                "required": ["input_path", "srt_path", "output_path"]
            }
        },
        handler=add_subtitles,
    )
    ctx.register_tool(
        name="video_editor_generate_tts",
        toolset="video_editor",
        schema={
            "name": "video_editor_generate_tts",
            "description": "Generate Text-to-Speech audio from text using Google Cloud. Provide text and output_path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to convert to speech."},
                    "output_path": {"type": "string", "description": "The path to save the generated MP3."},
                    "voice_name": {"type": "string", "description": "The voice name to use (e.g., \"pl-PL-Standard-B\").", "default": "pl-PL-Standard-B"},
                },
                "required": ["text", "output_path"]
            }
        },
        handler=generate_gcp_tts,
    )
    ctx.register_tool(
        name="video_editor_assemble_reel",
        toolset="video_editor",
        schema={
            "name": "video_editor_assemble_reel",
            "description": "Assemble multiple video clips and an audio track into a single reel (9:16). Provide video_paths (list), audio_path, output_path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_paths": {"type": "array", "items": {"type": "string"}, "description": "List of paths (or URLs) to video clips."},
                    "audio_path": {"type": "string", "description": "Path to the audio track."},
                    "output_path": {"type": "string", "description": "Path to save the final reel."},
                },
                "required": ["video_paths", "audio_path", "output_path"]
            }
        },
        handler=assemble_reel_moviepy,
    )
