from .directors import run_ceo_agent, run_cmo_agent
from .workers import generate_video_reel, build_funnel_systeme_io, seo_analysis
import json

def dispatch(task_description: str) -> dict:
    """
    Serce Hermesa (Orchestrator).
    Przyjmuje polecenie od użytkownika i uruchamia łańcuch wywołań Zarządu.
    """
    logs = []
    logs.append(f"👨‍💼 [WŁAŚCICIEL]: Zlecono nowe zadanie: {task_description}")
    
    # 1. CEO AI rozbija na plan
    logs.append("🧠 [CEO AI]: Analizuję i przygotowuję strategię...")
    ceo_plan = run_ceo_agent(task_description)
    logs.append(f"📄 [CEO AI PLAN]:\n{ceo_plan}")
    
    # 2. CMO AI interpretuje plan i wybiera narzędzia
    logs.append("🎯 [CMO AI]: Dobieram specjalistów i narzędzia do wykonania planu...")
    cmo_result = run_cmo_agent(ceo_plan)
    logs.append(f"📊 [CMO AI DECYZJA]: Wymagane narzędzia: {cmo_result['tools_to_run']}")
    
    # 3. Uruchamianie Robotników (Workers)
    worker_results = []
    
    for tool in cmo_result["tools_to_run"]:
        if tool == "video":
            logs.append("🎬 [VIDEO MAKER]: Wyszukuję materiały B-Roll w Pexels...")
            # Ekstrakcja słowa kluczowego (mock)
            keyword = "AI technology" if "AI" in task_description else "business"
            vid_res = generate_video_reel(keyword, count=2)
            worker_results.append(f"[WYNIK VIDEO]: {vid_res}")
            logs.append("✅ [VIDEO MAKER]: Zakończono.")
            
        elif tool == "funnel":
            logs.append("🌐 [FUNNEL BUILDER]: Buduję lejek w Systeme.io...")
            funnel_res = build_funnel_systeme_io("Holistic_Lejek_1", "<h1>Lejek</h1>")
            worker_results.append(f"[WYNIK LEJKA]: {funnel_res}")
            logs.append("✅ [FUNNEL BUILDER]: Zakończono.")
            
        elif tool == "seo":
            logs.append("📈 [SEO SPECIALIST]: Wykonuję analizę...")
            seo_res = seo_analysis("ADHD business")
            worker_results.append(f"[WYNIK SEO]: {seo_res}")
            logs.append("✅ [SEO SPECIALIST]: Zakończono.")
            
    # 4. Podsumowanie
    logs.append("🏢 [HERMES OS]: Zadanie zakończone. Wyniki przekazane do wglądu.")
    
    return {
        "status": "success",
        "logs": logs,
        "worker_results": worker_results
    }
