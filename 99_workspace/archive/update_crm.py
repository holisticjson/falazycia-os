import re

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Sidebar button
content = content.replace(
    'if st.button("💼 CRM Leads", use_container_width=True, type="primary" if col_menu == "CRM" else "secondary"):',
    'if st.button("💼 Holistic Broker CRM", use_container_width=True, type="primary" if col_menu == "CRM" else "secondary"):'
)

# 2. Extract and replace the CRM block
crm_pattern = re.compile(r'elif menu == "CRM":\s*\n.*?# 6\. ADHD KANBAN', re.DOTALL)

new_crm_block = '''elif menu == "CRM":
    st.title("💼 Holistic Broker CRM")
    st.subheader("B2B Lead Generation & Acquisitions Pipeline")
    
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #7C3AED;">
        <h3 style="margin-top: 0; color: #7C3AED;">💼 Dual-Engine B2B CRM</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            Miejsce dowodzenia dla AI Architekta (tomasz@holisticjson.pl) oraz projektów akwizycyjnych (tomasz@holistycznybroker.pl).
            Śledź statusy negocjacji bez zbędnego szumu.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    crm = load_crm()
    
    tab_board, tab_add = st.tabs(["📊 Tablica Lejka B2B", "➕ Zarejestruj Leada"])
    
    with tab_add:
        st.markdown("### ➕ Dodaj nowy Lead (AI / Nieruchomości)")
        new_name = st.text_input("Imię i Nazwisko / Nazwa Firmy:")
        new_notes = st.text_area("Szczegóły (Projekt, Budżet, Ból operacyjny, Notatki):")
        new_action = st.text_input("Następny Krok (Next Action):", placeholder="Np. Wysłać umowę NDA...")
        lead_type = st.radio("Typ Zlecenia:", ["AI Agency (Holistic Jason)", "Real Estate/Acquisition (Holistic Broker)"])
        
        if st.button("Zapisz w CRM", type="primary"):
            if new_name and new_notes:
                new_id = f"lead_{int(time.time())}"
                new_lead = {
                    "id": new_id,
                    "name": new_name,
                    "stage": "nowe_leady",
                    "notes": f"[{lead_type}] {new_notes}",
                    "last_contact": time.strftime("%Y-%m-%d"),
                    "next_action": new_action if new_action else "Ocena potencjału",
                    "draft_reply": f"Cześć {new_name.split()[0] if len(new_name.split()) > 0 else new_name}, przygotowałem propozycję rozwiązania..."
                }
                crm["leads"].append(new_lead)
                save_crm(crm)
                st.success(f"Lead {new_name} został dodany do bazy!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Podaj nazwę klienta oraz jego opis.")
                
    with tab_board:
        col_new, col_offer, col_neg, col_done = st.columns(4)
        
        # Backward compatibility with old stages
        new_leads = [l for l in crm["leads"] if l.get("stage") in ["nowe_leady", "conversation"]]
        offer_leads = [l for l in crm["leads"] if l.get("stage") in ["oferta", "architecture"]]
        neg_leads = [l for l in crm["leads"] if l.get("stage") == "negocjacje"]
        done_leads = [l for l in crm["leads"] if l.get("stage") in ["zrealizowane", "build", "archive"]]
        
        def render_lead_card(lead, col_obj, color, stage_name, next_stage_key, next_stage_val):
            with col_obj:
                st.markdown(f"""
                <div class="custom-card" style="border-left: 4px solid {color}; margin-bottom: 12px; padding: 10px;">
                    <span style="font-size: 0.75rem; color:#94A3B8;">📞 {lead.get('last_contact')}</span>
                    <h5 style="margin-top: 4px; margin-bottom: 6px; color: #FFFFFF; font-size: 1rem;">{lead.get('name')}</h5>
                    <p style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.3;">{lead.get('notes')[:80]}...</p>
                    <hr style="border-color: #1F242E; margin: 8px 0;">
                    <span style="font-size: 0.8rem; color: {color};">➡️ <strong>{lead.get('next_action')}</strong></span>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🔍 Ot", key=f"sel_{lead['id']}"):
                        st.session_state.selected_lead_id = lead['id']
                        st.rerun()
                with c2:
                    if next_stage_val:
                        if st.button("➡️ Dalej", key=f"mov_{next_stage_key}_{lead['id']}"):
                            lead["stage"] = next_stage_val
                            save_crm(crm)
                            st.rerun()

        with col_new:
            st.markdown("##### 📥 Nowe Leady")
            for lead in new_leads:
                render_lead_card(lead, st, "#3B82F6", "Nowe Leady", "offer", "oferta")
        with col_offer:
            st.markdown("##### 📄 Wysłana Oferta")
            for lead in offer_leads:
                render_lead_card(lead, st, "#F59E0B", "Wysłana Oferta", "neg", "negocjacje")
        with col_neg:
            st.markdown("##### 🤝 Negocjacje")
            for lead in neg_leads:
                render_lead_card(lead, st, "#EC4899", "Negocjacje", "done", "zrealizowane")
        with col_done:
            st.markdown("##### 🏆 Zrealizowane")
            for lead in done_leads:
                render_lead_card(lead, st, "#10B981", "Zrealizowane", "arch", None)

    # Szczegółowy podgląd wybranego klienta
    if "selected_lead_id" in st.session_state and st.session_state.selected_lead_id:
        sel_id = st.session_state.selected_lead_id
        lead = next((l for l in crm["leads"] if l["id"] == sel_id), None)
        
        if lead:
            st.markdown("---")
            st.subheader(f"💼 Focus Panel: {lead['name']}")
            
            c_det1, c_det2 = st.columns([1, 1])
            
            with c_det1:
                st.markdown(f"""
                <div class="custom-card" style="border-left: 5px solid #7C3AED;">
                    <h4>📋 Informacje o CRM</h4>
                    <p><strong>Notatki:</strong><br>{lead['notes']}</p>
                    <p><strong>Ostatni kontakt:</strong> {lead['last_contact']}</p>
                    <p><strong>Następny krok:</strong> <span class="focus-accent">{lead['next_action']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("##### Sterowanie:")
                col_stg1, col_stg2, col_stg3 = st.columns(3)
                with col_stg1:
                    if st.button("Cofnij Etap", key="btn_move_back"):
                        # Prosta logika cofania
                        if lead["stage"] == "oferta": lead["stage"] = "nowe_leady"
                        elif lead["stage"] == "negocjacje": lead["stage"] = "oferta"
                        elif lead["stage"] == "zrealizowane": lead["stage"] = "negocjacje"
                        save_crm(crm)
                        st.rerun()
                with col_stg2:
                    if st.button("🗑️ Usuń", key="btn_del_lead"):
                        crm["leads"] = [l for l in crm["leads"] if l["id"] != sel_id]
                        save_crm(crm)
                        st.session_state.selected_lead_id = None
                        st.rerun()
                with col_stg3:
                    if st.button("❌ Zamknij", key="btn_close_lead"):
                        st.session_state.selected_lead_id = None
                        st.rerun()
                        
            with c_det2:
                st.markdown("""
                <div class="custom-card" style="border-left: 5px solid #10B981; background-color: #0F1D1A;">
                    <h4 style="margin: 0; color: #10B981;">✉️ Draft Maila Akwizycyjnego (Cold Email)</h4>
                </div>
                """, unsafe_allow_html=True)
                
                modified_reply = st.text_area("Edytuj draft:", value=lead.get("draft_reply", ""), height=200)
                if st.button("Zapisz Draft", key=f"save_draft_{lead['id']}"):
                    lead["draft_reply"] = modified_reply
                    save_crm(crm)
                    st.toast("Odpowiedź zapisana!")

# 6. ADHD KANBAN'''

content = crm_pattern.sub(new_crm_block, content)

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("CRM updated successfully in app.py")
