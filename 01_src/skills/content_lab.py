import streamlit as st
import os
from pathlib import Path
import subprocess
from datetime import datetime

def render_content_lab():
    st.header("🎬 Content Lab — Fabryka Viralowych Treści")
    st.caption("Automatyczny montaż, wycinanie ciszy i neonowe napisy.")
    
    root = Path(r"c:\Aplikacje MVP\Holistic Jason")
    nuggets_dir = root / "04-ghost" / "nuggets"
    raw_dir = root / "04-ghost" / "raw_samples"
    output_dir = root / "generated_media" / "faceless"
    
    # Ensure dirs exist
    nuggets_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Wybierz materiał źródłowy")
        all_files = list(nuggets_dir.glob("*.mp3")) + list(nuggets_dir.glob("*.mp4")) + list(raw_dir.glob("*.*"))
        file_options = {f.name: f for f in all_files}
        
        selected_file_name = st.selectbox("Wybierz plik do obróbki:", list(file_options.keys()))
        selected_file_path = file_options.get(selected_file_name)
        
        if selected_file_path:
            st.info(f"Typ: {selected_file_path.suffix.upper()} | Wielkość: {selected_file_path.stat().st_size / 1024 / 1024:.2f} MB")
            
            if selected_file_path.suffix.lower() in ['.mp3', '.wav']:
                st.audio(str(selected_file_path))
            elif selected_file_path.suffix.lower() == '.mp4':
                st.video(str(selected_file_path))

    with col2:
        st.subheader("⚙️ Operacje AI")
        
        mode = st.radio("Wybierz tryb:", ["Auto-Trim (Cięcie ciszy)", "Full Viral (Cięcie + Napisy)"])
        
        if st.button("🚀 URUCHOM PROCES", type="primary", use_container_width=True):
            if not selected_file_path:
                st.error("Wybierz plik!")
                return
            
            with st.status("Przetwarzanie materiału...", expanded=True) as status:
                # 1. Auto-Trim
                st.write("🔍 Szukanie ciszy i wycinanie (PRO-CUT)...")
                try:
                    from skills.auto_trimmer import auto_trim_silence
                    tight_output_name = f"{selected_file_path.stem}_tight_pro{selected_file_path.suffix}"
                    tight_path = auto_trim_silence(selected_file_path, tight_output_name)
                    st.write(f"✅ Wycięto ciszę. Nowy plik: `{tight_output_name}`")
                except Exception as e:
                    st.error(f"Błąd Auto-Trimmer: {e}")
                    return
                
                if mode == "Full Viral (Cięcie + Napisy)":
                    st.write("📝 Generowanie transkrypcji i napisów...")
                    # Here we would call the transcription and burn logic
                    # For now, we point to the result of our previous hard work
                    st.write("🎬 Składanie wideo i wypalanie neonów...")
                    st.info("W tej wersji dashboardu używamy zoptymalizowanego skryptu final_pro_render.py")
                    
                    # Run the final render script
                    # (In production, this would be more dynamic)
                    subprocess.run(["python", str(root / "final_pro_render.py")], check=True)
                
                status.update(label="✅ Proces zakończony!", state="complete")
                st.success("Twój materiał jest gotowy!")
                
    st.divider()
    st.subheader("📺 Ostatnio wygenerowane")
    
    # List files in output dir
    generated_videos = list(output_dir.glob("*.mp4"))
    generated_videos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for vid in generated_videos[:3]:
        with st.expander(f"🎬 {vid.name} ({datetime.fromtimestamp(vid.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})"):
            st.video(str(vid))
            col_dl, col_del = st.columns(2)
            with col_dl:
                with open(vid, "rb") as f:
                    st.download_button("💾 Pobierz", f, file_name=vid.name, use_container_width=True)
            with col_del:
                if st.button(f"🗑️ Usuń {vid.name}", key=vid.name):
                    vid.unlink()
                    st.rerun()

if __name__ == "__main__":
    # Test render
    render_content_lab()
