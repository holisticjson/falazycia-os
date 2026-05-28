import streamlit as st
import json
import base64
from datetime import datetime
import io
from streamlit_paste_button import paste_image_button as pbutton

# Słownik 7 Promptów Executive Function wg materiałów Claude
ADHD_PROMPTS = {
    "task_paralysis": {
        "title": "⚡ 1. Break Task Paralysis",
        "description": "Rozbij zadanie, za które nie możesz się zabrać, na pierwsze kroki < 60 sek.",
        "template": 'I am staring at "{task}" and cannot make myself start. Break it down into steps so small that each one takes under 60 seconds to complete. Give me only the very first step and tell me exactly what to do with my hands right now to begin.'
    },
    "dopamine_menu": {
        "title": "🍔 2. Build a Dopamine Menu",
        "description": "Wygeneruj menu 5-20 min aktywności stymulujących, gdy mózg jest niedostymulowany.",
        "template": "My brain is understimulated and I am losing focus. Build me a Dopamine Menu with three sections: 5-minute Starters for quick physical movement, 20-minute Main Tasks for deep focused work, and 10-minute Side Activities for creative play. Give me enough options in each section that I can rotate through them and stay engaged all day."
    },
    "body_double": {
        "title": "👥 3. Use Claude as a Body Double",
        "description": "Wirtualny partner do pracy, który sprawdzi postępy co 10 minut.",
        "template": "Be my body double for the next 30 minutes. I am working on \"{task}\". Check in with me every 10 minutes, ask what I have done since the last check-in, and pull me back on track if I have gone off course."
    },
    "task_reset": {
        "title": "♻️ 4. Reset Between Tasks",
        "description": "Protokół resetu mózgu między drastycznie różnymi zadaniami.",
        "template": "I just finished \"{task_a}\" and need to move into \"{task_b}\" but my brain will not switch gears. Design a 3-minute reset routine that clears the mental residue from the first task and prepares my focus for the completely different energy the second one requires."
    },
    "gamify": {
        "title": "🎮 5. Gamify the Boring Stuff",
        "description": "Zamień nudne zadanie w misję z nagrodami (Quest).",
        "template": "I have a boring task I keep avoiding: \"{task}\". Connect it to something I am currently obsessed with: \"{interest}\". Build a Quest structure around it where completing each part unlocks a specific reward and finishing the whole thing means something actually worth working toward."
    },
    "time_blindness": {
        "title": "⏳ 6. Fix Time Blindness",
        "description": "Znajdź 'ukryte' mikrozadania, o których zapomniałeś, by urealnić czas wykonania.",
        "template": "I keep telling myself \"{project}\" will take 20 minutes and then it takes 2 hours. Help me time-map this realistically by identifying the 3 hidden sub-tasks I always forget to account for so I can set a deadline that is actually accurate."
    },
    "open_loops": {
        "title": "🗑️ 7. Clear Your Open Loops",
        "description": "Wyrzuć z głowy cały chaos. Model podzieli go na Teraz, Potem i Śmietnik.",
        "template": "My brain is overloaded with open loops. I am going to dump everything I am anxious about below. Sort everything into three categories: Now, Later, and Trash. Then write one clear actionable next step for every item in the Now category only.\n\n[DUMP]:\n{dump}"
    }
}

@st.dialog("💀 Czaszka: Ingestion Hub & Brain Dump")
def render_floating_skull_dialog():
    """Wyskakujące okienko do zrzutu myśli, linków i obrazów z każdego miejsca w aplikacji"""
    st.markdown("### Wyrzuć to z głowy, zajmiemy się tym!")
    
    dump_text = st.text_area("Co Ci chodzi po głowie? (Zmartwienia, zadania, myśli)", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        links_text = st.text_area("Wklej linki / źródła (Inspiracje):", height=100, placeholder="https://...")
    with col2:
        uploaded_image = st.file_uploader("Dodaj zrzut ekranu (opcjonalnie):", type=["png", "jpg", "jpeg"])
        paste_result = pbutton("📋 Wklej ze schowka (Schowek -> Kliknij)")
        
    if st.button("🧠 Czyść Pętle (Clear Open Loops)", type="primary", use_container_width=True):
        if not dump_text and not links_text and not uploaded_image and (paste_result.image_data is None):
            st.warning("Musisz podać jakiś materiał (tekst, link lub obraz)!")
            return
            
        with st.spinner("Model porządkuje Twój chaos (Teraz, Potem, Śmietnik)..."):
            # Format payload for the LLM
            combined_dump = dump_text
            if links_text:
                combined_dump += f"\n\nLINKI/ŹRÓDŁA:\n{links_text}"
                
            prompt = ADHD_PROMPTS["open_loops"]["template"].format(dump=combined_dump)
            
            # W tym miejscu wywołamy klienta Gemini lub Claude (przekazany z sesji lub jako import)
            # Użyjemy session state by trzymać wyniki
            st.session_state.last_skull_prompt = prompt
            if uploaded_image:
                # Jeśli jest obraz z uploader'a
                bytes_data = uploaded_image.getvalue()
                st.session_state.last_skull_image = bytes_data
            elif paste_result.image_data is not None:
                # Jeśli jest wklejony ze schowka
                img_byte_arr = io.BytesIO()
                paste_result.image_data.save(img_byte_arr, format='PNG')
                st.session_state.last_skull_image = img_byte_arr.getvalue()
            else:
                st.session_state.last_skull_image = None
                
            st.session_state.trigger_skull_analysis = True
            st.rerun()

def render_executive_function_menu(client=None):
    """Renderuje główne menu 7 promptów ratunkowych w ADHD Command Center"""
    st.markdown("### 🧠 The ADHD Executive Function Mode (Gemini 2.5 Powered)")
    st.caption("Wyselekcjonowane protokoły ratunkowe dla dysfunkcji wykonawczych (kora przedczołowa).")
    
    tabs = st.tabs([
        "⚡ Task Paralysis", "🍔 Dopamine Menu", "👥 Body Double", 
        "♻️ Task Reset", "🎮 Gamify", "⏳ Time Blindness"
    ])
    
    with tabs[0]:
        st.markdown(f"**{ADHD_PROMPTS['task_paralysis']['description']}**")
        task_input = st.text_input("Jakie zadanie Cię paraliżuje?", key="tp_task")
        if st.button("Rozbij na kroki", key="btn_tp"):
            p = ADHD_PROMPTS['task_paralysis']['template'].format(task=task_input)
            st.session_state.adhd_exec_prompt = p
            st.rerun()
            
    with tabs[1]:
        st.markdown(f"**{ADHD_PROMPTS['dopamine_menu']['description']}**")
        if st.button("Zbuduj Dopamine Menu", key="btn_dm"):
            p = ADHD_PROMPTS['dopamine_menu']['template']
            st.session_state.adhd_exec_prompt = p
            st.rerun()
            
    with tabs[2]:
        st.markdown(f"**{ADHD_PROMPTS['body_double']['description']}**")
        task_bd = st.text_input("Nad czym będziesz teraz pracować przez 30 min?", key="bd_task")
        if st.button("Aktywuj Body Double (Gemini)", key="btn_bd"):
            p = ADHD_PROMPTS['body_double']['template'].format(task=task_bd)
            st.session_state.adhd_exec_prompt = p
            st.rerun()
            
    with tabs[3]:
        st.markdown(f"**{ADHD_PROMPTS['task_reset']['description']}**")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            t_a = st.text_input("Zadanie, które WŁAŚNIE skończyłeś:", key="tr_a")
        with col_r2:
            t_b = st.text_input("Zadanie, które MUSISZ teraz zacząć:", key="tr_b")
        if st.button("Wygeneruj 3-min Protokół Resetu", key="btn_tr"):
            p = ADHD_PROMPTS['task_reset']['template'].format(task_a=t_a, task_b=t_b)
            st.session_state.adhd_exec_prompt = p
            st.rerun()
            
    with tabs[4]:
        st.markdown(f"**{ADHD_PROMPTS['gamify']['description']}**")
        t_boring = st.text_input("Nudne zadanie, którego unikasz:", key="gf_b")
        t_interest = st.text_input("Twoja obecna hiperfiksacja / zajawka (np. Elden Ring, Kosmos, Lego):", key="gf_i")
        if st.button("Stwórz Quest", key="btn_gf"):
            p = ADHD_PROMPTS['gamify']['template'].format(task=t_boring, interest=t_interest)
            st.session_state.adhd_exec_prompt = p
            st.rerun()
            
    with tabs[5]:
        st.markdown(f"**{ADHD_PROMPTS['time_blindness']['description']}**")
        t_proj = st.text_input("Co rzekomo zajmie Ci 'tylko 20 minut'?", key="tb_p")
        if st.button("Urealnij Czas (Time-Map)", key="btn_tb"):
            p = ADHD_PROMPTS['time_blindness']['template'].format(project=t_proj)
            st.session_state.adhd_exec_prompt = p
            st.rerun()

    # Sekcja wykonania promptu bezpośrednio pod zakładkami
    if "adhd_exec_prompt" in st.session_state and st.session_state.adhd_exec_prompt:
        st.divider()
        st.markdown('<div class="inflow-card ceo-accent" style="border: 1px solid rgba(16,185,129,0.3); padding: 20px; border-radius:12px; background: rgba(16,185,129,0.02);">', unsafe_allow_html=True)
        st.markdown("### 🤖 Asystent Kognitywny: Generuję rozwiązanie...")
        
        if client:
            with st.spinner("Przetwarzanie protokołu kognitywnego (Gemini 2.5 Flash)..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=st.session_state.adhd_exec_prompt
                    )
                    st.success("✅ Protokół kognitywny gotowy! Użyj go, aby odblokować skupienie.")
                    st.markdown(response.text)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🏆 Wykonałem to! (+25 pkt Dopamine Boost)", use_container_width=True, type="primary"):
                        if "save_dopamine_win_fn" in st.session_state and st.session_state.save_dopamine_win_fn:
                            st.session_state.save_dopamine_win_fn("🔥 Zadanie", "Ukończono protokół kognitywny ADHD", 25)
                            st.toast("🎉 Zarejestrowano +25 pkt!")
                            st.session_state.adhd_exec_prompt = None
                            st.rerun()
                except Exception as e:
                    st.error(f"Błąd generowania protokołu: {e}")
        else:
            st.warning("⚠️ Brak klienta API do wykonania promptu!")
            st.markdown(f"**Twój przygotowany prompt:** {st.session_state.adhd_exec_prompt}")
            
        if st.button("❌ Zamknij Protokół Kognitywny", use_container_width=True):
            st.session_state.adhd_exec_prompt = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
