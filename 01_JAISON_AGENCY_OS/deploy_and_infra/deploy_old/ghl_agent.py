"""
🔌 GHL Agent v2 — Zarządzanie Go High Level przez API v2
Base URL: services.leadconnectorhq.com
Auth: Private Integration Token + Version header
Pełne Scopes: contacts, conversations, calendars, pipelines, workflows, users, locations
"""
import streamlit as st
import requests
import json
from datetime import datetime

GHL_BASE = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

def ghl_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Version": API_VERSION,
    }

def ghl_get(endpoint, api_key, params=None):
    r = requests.get(f"{GHL_BASE}/{endpoint}", headers=ghl_headers(api_key), params=params, timeout=15)
    return r.json() if r.ok else {"error": r.status_code, "detail": r.text[:300]}

def ghl_post(endpoint, api_key, data=None):
    r = requests.post(f"{GHL_BASE}/{endpoint}", headers=ghl_headers(api_key), json=data, timeout=15)
    return r.json() if r.ok else {"error": r.status_code, "detail": r.text[:300]}

def ghl_put(endpoint, api_key, data=None):
    r = requests.put(f"{GHL_BASE}/{endpoint}", headers=ghl_headers(api_key), json=data, timeout=15)
    return r.json() if r.ok else {"error": r.status_code, "detail": r.text[:300]}

def ghl_delete(endpoint, api_key):
    r = requests.delete(f"{GHL_BASE}/{endpoint}", headers=ghl_headers(api_key), timeout=15)
    return r.json() if r.ok else {"error": r.status_code, "detail": r.text[:300]}

# ======================================================================
# AKCJE GHL — pełna lista
# ======================================================================
GHL_ACTIONS = {
    "👥 Szukaj kontaktów": "contacts_search",
    "➕ Dodaj kontakt": "contact_add",
    "✏️ Edytuj kontakt": "contact_edit",
    "🏷️ Dodaj/Usuń tag": "contact_tag",
    "📊 Pipelines / Lejki": "pipelines",
    "🎯 Opportunities (Szanse)": "opportunities",
    "📅 Kalendarze": "calendars",
    "💬 Konwersacje": "conversations",
    "📩 Wyślij wiadomość": "send_message",
    "⚙️ Workflows": "workflows",
    "📍 Info o lokalizacji": "location_info",
    "👤 Użytkownicy": "users",
    "📋 Custom Fields": "custom_fields",
    "📝 Notatki kontaktu": "contact_notes",
    "📞 Zadania kontaktu": "contact_tasks",
    "───── SOCIAL MEDIA ─────": "_sep1",
    "📱 Social Media — Konta": "sm_accounts",
    "✍️ Social Media — Publikuj post": "sm_post",
    "📊 Social Media — Statystyki": "sm_stats",
    "───── BRANDING & CONTENT ─────": "_sep2",
    "🎨 Brand Board": "brand_board",
    "✉️ Szablony Email": "email_templates",
    "📝 Blog — Publikuj post": "blog_post",
    "📄 Formularze": "forms",
    "───── LEJKI & PRODUKTY ─────": "_sep3",
    "🔗 Funnels / Lejki (podgląd)": "funnels",
    "🛒 Produkty": "products",
    "🧾 Faktury": "invoices",
    "📎 Media (upload)": "media_upload",
}

def render_ghl_agent():
    """Renderuje panel GHL Agent v2"""
    import os
    st.header("🔌 GHL Agent v2 — Go High Level API")
    st.caption("Pełne zarządzanie GHL przez API v2. Private Integration z pełnymi Scopes.")
    
    # Domyślne wartości z env vars (Cloud Run) lub session_state
    default_token = os.environ.get("GHL_API_TOKEN", "")
    default_location = os.environ.get("GHL_LOCATION_ID", "")
    
    if "ghl_token" not in st.session_state:
        st.session_state.ghl_token = default_token
    if "ghl_location" not in st.session_state:
        st.session_state.ghl_location = default_location
    
    # API Key + Location ID (z możliwością edycji)
    with st.expander("🔑 Dane dostępowe GHL", expanded=not st.session_state.ghl_token):
        col_k1, col_k2 = st.columns([3, 2])
        with col_k1:
            token = st.text_input("Private Integration Token:", value=st.session_state.ghl_token, type="password")
        with col_k2:
            loc_id = st.text_input("Location ID:", value=st.session_state.ghl_location)
        if st.button("💾 Zapisz na stałe w sesji"):
            st.session_state.ghl_token = token
            st.session_state.ghl_location = loc_id
            st.success("✅ Zapisano! Nie musisz wpisywać ponownie.")
            st.rerun()
    
    api_key = st.session_state.ghl_token or token
    location_id = st.session_state.ghl_location or loc_id
    action = st.selectbox("Akcja:", list(GHL_ACTIONS.keys()))
    action_key = GHL_ACTIONS[action]
    
    # --- KONTAKTY: SZUKAJ ---
    if action_key == "contacts_search":
        with st.form("search_contacts"):
            query = st.text_input("Szukaj (imię, email, telefon):", placeholder="Jan Kowalski")
            limit = st.slider("Limit wyników:", 5, 100, 20)
            if st.form_submit_button("🔍 Szukaj", type="primary", use_container_width=True):
                with st.spinner("Szukam..."):
                    params = {"locationId": location_id, "limit": limit}
                    if query:
                        params["query"] = query
                    result = ghl_get("contacts/search", api_key, params)
                    if "contacts" in result:
                        contacts = result["contacts"]
                        st.success(f"Znaleziono {len(contacts)} kontaktów")
                        for c in contacts:
                            cid = c.get("id", "")
                            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                            email = c.get("email", "-")
                            phone = c.get("phone", "-")
                            tags = ", ".join(c.get("tags", []))
                            st.markdown(f"**{name}** | {email} | {phone} | Tags: `{tags}` | ID: `{cid[:12]}...`")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- KONTAKTY: DODAJ ---
    elif action_key == "contact_add":
        with st.form("add_contact"):
            col1, col2 = st.columns(2)
            with col1:
                fname = st.text_input("Imię *")
                lname = st.text_input("Nazwisko")
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Telefon")
                company = st.text_input("Firma")
                source = st.text_input("Źródło", value="Holistic CEO Agent")
            tags_input = st.text_input("Tagi (po przecinku)", placeholder="Lead, Diagnoza AI, Premium")
            if st.form_submit_button("➕ Dodaj kontakt", type="primary", use_container_width=True):
                data = {"firstName": fname, "lastName": lname, "email": email,
                        "phone": phone, "companyName": company, "source": source,
                        "locationId": location_id}
                if tags_input:
                    data["tags"] = [t.strip() for t in tags_input.split(",") if t.strip()]
                with st.spinner("Dodaję..."):
                    result = ghl_post("contacts/", api_key, data)
                    if "contact" in result:
                        st.success(f"✅ Kontakt {fname} dodany! ID: {result['contact']['id']}")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- KONTAKTY: EDYTUJ ---
    elif action_key == "contact_edit":
        with st.form("edit_contact"):
            contact_id = st.text_input("Contact ID *")
            col1, col2 = st.columns(2)
            with col1:
                fname = st.text_input("Nowe imię (puste = bez zmian)")
                email = st.text_input("Nowy email")
            with col2:
                phone = st.text_input("Nowy telefon")
                company = st.text_input("Nowa firma")
            if st.form_submit_button("✏️ Zapisz zmiany", type="primary", use_container_width=True):
                data = {}
                if fname: data["firstName"] = fname
                if email: data["email"] = email
                if phone: data["phone"] = phone
                if company: data["companyName"] = company
                with st.spinner("Aktualizuję..."):
                    result = ghl_put(f"contacts/{contact_id}", api_key, data)
                    if "contact" in result:
                        st.success("✅ Kontakt zaktualizowany!")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- KONTAKTY: TAGI ---
    elif action_key == "contact_tag":
        with st.form("tag_form"):
            contact_id = st.text_input("Contact ID *")
            tags_input = st.text_input("Tagi (po przecinku) *")
            tag_action = st.radio("Operacja:", ["Dodaj tagi", "Usuń tagi"], horizontal=True)
            if st.form_submit_button("🏷️ Wykonaj", type="primary", use_container_width=True):
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                with st.spinner("Pracuję..."):
                    if tag_action == "Dodaj tagi":
                        result = ghl_post(f"contacts/{contact_id}/tags", api_key, {"tags": tags})
                    else:
                        result = ghl_delete(f"contacts/{contact_id}/tags", api_key)
                    if "error" not in result:
                        st.success(f"✅ Tagi {tag_action.lower()}: {tags}")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- PIPELINES ---
    elif action_key == "pipelines":
        if st.button("📊 Pobierz lejki", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("opportunities/pipelines", api_key, {"locationId": location_id})
                if "pipelines" in result:
                    for p in result["pipelines"]:
                        st.markdown(f"### 📊 {p['name']} (ID: `{p['id'][:12]}...`)")
                        for stage in p.get("stages", []):
                            st.markdown(f"  - **{stage['name']}** (ID: `{stage['id'][:12]}...`)")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- OPPORTUNITIES ---
    elif action_key == "opportunities":
        with st.form("opps_form"):
            pipeline_id = st.text_input("Pipeline ID *")
            if st.form_submit_button("🎯 Pobierz szanse", type="primary", use_container_width=True):
                with st.spinner("Pobieram..."):
                    result = ghl_get("opportunities/search", api_key, 
                                     {"location_id": location_id, "pipeline_id": pipeline_id})
                    if "opportunities" in result:
                        for opp in result["opportunities"]:
                            name = opp.get("name", "Bez nazwy")
                            value = opp.get("monetaryValue", 0)
                            stage = opp.get("pipelineStageId", "-")
                            status = opp.get("status", "-")
                            st.markdown(f"🎯 **{name}** | {value} PLN | Status: `{status}`")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- KALENDARZE ---
    elif action_key == "calendars":
        if st.button("📅 Pobierz kalendarze", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("calendars/", api_key, {"locationId": location_id})
                if "calendars" in result:
                    for cal in result["calendars"]:
                        st.markdown(f"📅 **{cal['name']}** | ID: `{cal['id'][:12]}...`")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- KONWERSACJE ---
    elif action_key == "conversations":
        if st.button("💬 Pobierz konwersacje", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("conversations/search", api_key, {"locationId": location_id, "limit": 20})
                if "conversations" in result:
                    for conv in result["conversations"][:15]:
                        name = conv.get("contactName", conv.get("fullName", "Nieznany"))
                        last_msg = conv.get("lastMessageBody", "")[:80]
                        cid = conv.get("contactId", "")
                        st.markdown(f"💬 **{name}**: _{last_msg}_ | Contact: `{cid[:12]}...`")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- WYŚLIJ WIADOMOŚĆ ---
    elif action_key == "send_message":
        with st.form("send_msg"):
            contact_id = st.text_input("Contact ID *")
            msg_type = st.selectbox("Typ:", ["SMS", "Email", "WhatsApp", "GMB", "IG", "FB"])
            subject = st.text_input("Temat (tylko Email)")
            message = st.text_area("Treść wiadomości *")
            if st.form_submit_button("📩 Wyślij", type="primary", use_container_width=True):
                data = {"type": msg_type, "contactId": contact_id, "message": message}
                if subject and msg_type == "Email":
                    data["subject"] = subject
                with st.spinner("Wysyłam..."):
                    result = ghl_post("conversations/messages", api_key, data)
                    if "error" not in result:
                        st.success("✅ Wiadomość wysłana!")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- WORKFLOWS ---
    elif action_key == "workflows":
        if st.button("⚙️ Pobierz workflows", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("workflows/", api_key, {"locationId": location_id})
                if "workflows" in result:
                    for wf in result["workflows"]:
                        status = "🟢" if wf.get("status") == "published" else "🔴"
                        st.markdown(f"{status} **{wf['name']}** | ID: `{wf['id'][:12]}...`")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- LOCATION INFO ---
    elif action_key == "location_info":
        if st.button("📍 Pobierz info", type="primary", use_container_width=True):
            if not location_id:
                st.error("Podaj Location ID")
                return
            with st.spinner("Pobieram..."):
                result = ghl_get(f"locations/{location_id}", api_key)
                if "location" in result:
                    loc = result["location"]
                    st.json(loc)
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- USERS ---
    elif action_key == "users":
        if st.button("👤 Pobierz użytkowników", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("users/search", api_key, {"locationId": location_id})
                if "users" in result:
                    for u in result["users"]:
                        name = f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()
                        email = u.get("email", "-")
                        role = u.get("role", "-")
                        st.markdown(f"👤 **{name}** | {email} | Rola: `{role}`")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- CUSTOM FIELDS ---
    elif action_key == "custom_fields":
        if st.button("📋 Pobierz pola", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get(f"locations/{location_id}/customFields", api_key)
                if "customFields" in result:
                    for cf in result["customFields"]:
                        st.markdown(f"📋 **{cf['name']}** | Typ: `{cf.get('dataType', '-')}` | ID: `{cf['id'][:12]}...`")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- NOTATKI ---
    elif action_key == "contact_notes":
        with st.form("notes_form"):
            contact_id = st.text_input("Contact ID *")
            note_text = st.text_area("Nowa notatka (puste = tylko pokaż istniejące)")
            if st.form_submit_button("📝 Wykonaj", type="primary", use_container_width=True):
                if note_text:
                    with st.spinner("Dodaję notatkę..."):
                        result = ghl_post(f"contacts/{contact_id}/notes", api_key, {"body": note_text})
                        if "error" not in result:
                            st.success("✅ Notatka dodana!")
                        else:
                            st.error(f"Błąd: {json.dumps(result, indent=2)}")
                else:
                    with st.spinner("Pobieram notatki..."):
                        result = ghl_get(f"contacts/{contact_id}/notes", api_key)
                        if "notes" in result:
                            for n in result["notes"]:
                                st.markdown(f"📝 {n.get('body', '')} | {n.get('dateAdded', '')}")
                        else:
                            st.error(f"Błąd: {json.dumps(result, indent=2)}")
    
    # --- ZADANIA ---
    elif action_key == "contact_tasks":
        with st.form("tasks_form"):
            contact_id = st.text_input("Contact ID *")
            task_title = st.text_input("Nowe zadanie (puste = tylko pokaż)")
            task_desc = st.text_area("Opis zadania")
            if st.form_submit_button("📞 Wykonaj", type="primary", use_container_width=True):
                if task_title:
                    with st.spinner("Dodaję zadanie..."):
                        result = ghl_post(f"contacts/{contact_id}/tasks", api_key, 
                                          {"title": task_title, "body": task_desc})
                        if "error" not in result:
                            st.success("✅ Zadanie dodane!")
                        else:
                            st.error(f"Błąd: {json.dumps(result, indent=2)}")
                else:
                    with st.spinner("Pobieram zadania..."):
                        result = ghl_get(f"contacts/{contact_id}/tasks", api_key)
                        if "tasks" in result:
                            for t in result["tasks"]:
                                st.markdown(f"📞 **{t.get('title', '')}** | {t.get('status', '')}")
                        else:
                            st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === SEPARATORY (skip) ===
    elif action_key.startswith("_sep"):
        st.info("Wybierz konkretną akcję z listy powyżej.")

    # === SOCIAL MEDIA — KONTA ===
    elif action_key == "sm_accounts":
        if st.button("📱 Pobierz konta SM", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("social-media-posting/oauth/", api_key, {"locationId": location_id})
                if isinstance(result, dict) and "error" not in result:
                    st.json(result)
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === SOCIAL MEDIA — PUBLIKUJ POST ===
    elif action_key == "sm_post":
        with st.form("sm_post_form"):
            st.subheader("📱 Publikuj post na Social Media")
            post_text = st.text_area("Treść posta *", height=150)
            col1, col2 = st.columns(2)
            with col1:
                platforms = st.multiselect("Platformy:", ["facebook", "instagram", "google", "linkedin", "tiktok", "twitter"])
            with col2:
                schedule = st.date_input("Data publikacji (puste = teraz)")
                schedule_time = st.time_input("Godzina")
            media_url = st.text_input("URL obrazka/wideo (opcjonalnie)")
            if st.form_submit_button("📱 Publikuj", type="primary", use_container_width=True):
                data = {
                    "locationId": location_id,
                    "post": post_text,
                    "type": "post",
                    "platforms": platforms,
                }
                if media_url:
                    data["mediaUrls"] = [media_url]
                with st.spinner("Publikuję..."):
                    result = ghl_post("social-media-posting/post/", api_key, data)
                    if isinstance(result, dict) and "error" not in result:
                        st.success("✅ Post opublikowany/zaplanowany!")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === SOCIAL MEDIA — STATYSTYKI ===
    elif action_key == "sm_stats":
        if st.button("📊 Pobierz statystyki SM", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("social-media-posting/post/", api_key, {"locationId": location_id, "limit": 20})
                if isinstance(result, dict) and "posts" in result:
                    for p in result["posts"]:
                        status = p.get("status", "-")
                        text = p.get("post", "")[:80]
                        platforms = ", ".join(p.get("platforms", []))
                        st.markdown(f"📱 **{status}** | {platforms} | _{text}_")
                else:
                    st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === BRAND BOARD ===
    elif action_key == "brand_board":
        tab1, tab2 = st.tabs(["🎨 Design Kit", "🗣️ Brand Voice"])
        with tab1:
            if st.button("Pobierz Design Kit", type="primary", use_container_width=True):
                with st.spinner("Pobieram..."):
                    result = ghl_get(f"brand-boards/design-kit", api_key, {"locationId": location_id})
                    st.json(result)
        with tab2:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Pobierz Brand Voice"):
                    with st.spinner("Pobieram..."):
                        result = ghl_get(f"brand-boards/voices", api_key, {"locationId": location_id})
                        st.json(result)
            with col2:
                with st.form("brand_voice_form"):
                    voice_name = st.text_input("Nazwa głosu marki")
                    voice_desc = st.text_area("Opis tonu (np. profesjonalny, ciepły, ekspercki)")
                    if st.form_submit_button("💾 Zapisz Brand Voice"):
                        with st.spinner("Zapisuję..."):
                            result = ghl_post("brand-boards/voices", api_key,
                                              {"locationId": location_id, "name": voice_name, "description": voice_desc})
                            if "error" not in result:
                                st.success("✅ Brand Voice zapisany!")
                            else:
                                st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === EMAIL TEMPLATES ===
    elif action_key == "email_templates":
        tab1, tab2 = st.tabs(["📋 Lista szablonów", "➕ Utwórz szablon"])
        with tab1:
            if st.button("Pobierz szablony email", type="primary", use_container_width=True):
                with st.spinner("Pobieram..."):
                    result = ghl_get("emails/builder", api_key, {"locationId": location_id, "limit": 20})
                    if "templates" in result:
                        for t in result["templates"]:
                            st.markdown(f"✉️ **{t.get('name', '')}** | ID: `{t.get('id', '')[:12]}...`")
                    else:
                        st.json(result)
        with tab2:
            with st.form("email_tpl_form"):
                tpl_name = st.text_input("Nazwa szablonu *")
                subject = st.text_input("Temat emaila *")
                html_body = st.text_area("HTML treści emaila *", height=200,
                    placeholder="<h1>Cześć {{contact.firstName}}</h1><p>Treść...</p>")
                if st.form_submit_button("➕ Utwórz szablon", type="primary"):
                    with st.spinner("Tworzę..."):
                        result = ghl_post("emails/builder", api_key,
                            {"locationId": location_id, "name": tpl_name,
                             "subject": subject, "htmlBody": html_body})
                        if "error" not in result:
                            st.success(f"✅ Szablon '{tpl_name}' utworzony!")
                        else:
                            st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === BLOG POST ===
    elif action_key == "blog_post":
        with st.form("blog_form"):
            st.subheader("📝 Publikuj post na blogu GHL")
            title = st.text_input("Tytuł posta *")
            slug = st.text_input("Slug (URL)", placeholder="moj-nowy-post")
            content = st.text_area("Treść (HTML) *", height=200)
            meta_desc = st.text_input("Meta description (SEO)")
            status = st.selectbox("Status:", ["published", "draft"])
            if st.form_submit_button("📝 Publikuj", type="primary", use_container_width=True):
                data = {
                    "locationId": location_id, "title": title, "slug": slug,
                    "content": content, "metaDescription": meta_desc, "status": status
                }
                with st.spinner("Publikuję..."):
                    result = ghl_post("blogs/post", api_key, data)
                    if "error" not in result:
                        st.success(f"✅ Post '{title}' opublikowany!")
                    else:
                        st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === FORMULARZE ===
    elif action_key == "forms":
        if st.button("📄 Pobierz formularze", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("forms/", api_key, {"locationId": location_id, "limit": 50})
                if "forms" in result:
                    for f in result["forms"]:
                        st.markdown(f"📄 **{f.get('name', '')}** | ID: `{f.get('id', '')[:12]}...`")
                else:
                    st.json(result)

    # === FUNNELS (readonly) ===
    elif action_key == "funnels":
        if st.button("🔗 Pobierz lejki", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("funnels/funnel/list", api_key, {"locationId": location_id, "limit": 20})
                if "funnels" in result:
                    for fn in result["funnels"]:
                        name = fn.get("name", "Bez nazwy")
                        steps = len(fn.get("steps", []))
                        url = fn.get("url", "-")
                        st.markdown(f"🔗 **{name}** | {steps} kroków | URL: `{url}`")
                        for step in fn.get("steps", []):
                            st.markdown(f"  └ {step.get('name', '')} — `{step.get('url', '')}`")
                else:
                    st.json(result)

    # === PRODUKTY ===
    elif action_key == "products":
        tab1, tab2 = st.tabs(["📋 Lista", "➕ Dodaj produkt"])
        with tab1:
            if st.button("Pobierz produkty", type="primary", use_container_width=True):
                with st.spinner("Pobieram..."):
                    result = ghl_get("products/", api_key, {"locationId": location_id})
                    if "products" in result:
                        for pr in result["products"]:
                            st.markdown(f"🛒 **{pr.get('name', '')}** | {pr.get('description', '')[:60]}")
                    else:
                        st.json(result)
        with tab2:
            with st.form("add_product"):
                p_name = st.text_input("Nazwa produktu *")
                p_desc = st.text_area("Opis")
                p_price = st.number_input("Cena (gr/centy)", min_value=0, value=9900)
                if st.form_submit_button("➕ Dodaj produkt", type="primary"):
                    with st.spinner("Dodaję..."):
                        result = ghl_post("products/", api_key,
                            {"locationId": location_id, "name": p_name, "description": p_desc})
                        if "error" not in result:
                            st.success(f"✅ Produkt '{p_name}' dodany!")
                        else:
                            st.error(f"Błąd: {json.dumps(result, indent=2)}")

    # === FAKTURY ===
    elif action_key == "invoices":
        if st.button("🧾 Pobierz faktury", type="primary", use_container_width=True):
            with st.spinner("Pobieram..."):
                result = ghl_get("invoices/", api_key, {"locationId": location_id, "limit": 20})
                if "invoices" in result:
                    for inv in result["invoices"]:
                        name = inv.get("name", inv.get("title", "Bez nazwy"))
                        amount = inv.get("amountDue", 0)
                        status = inv.get("status", "-")
                        st.markdown(f"🧾 **{name}** | {amount/100:.2f} PLN | Status: `{status}`")
                else:
                    st.json(result)

    # === MEDIA UPLOAD ===
    elif action_key == "media_upload":
        with st.form("media_form"):
            uploaded_files = st.file_uploader("Wybierz pliki", type=["png", "jpg", "jpeg", "gif", "svg", "mp4", "pdf"], accept_multiple_files=True)
            if st.form_submit_button("📎 Upload Hurtowy", type="primary", use_container_width=True):
                if uploaded_files:
                    headers = {"Authorization": f"Bearer {api_key}", "Version": API_VERSION}
                    for uploaded in uploaded_files:
                        with st.spinner(f"Uploaduję {uploaded.name}..."):
                            files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                            r = requests.post(f"{GHL_BASE}/medias/upload-file",
                                headers=headers, files=files,
                                data={"locationId": location_id}, timeout=30)
                            if r.ok:
                                st.success(f"✅ Plik '{uploaded.name}' wgany! URL: {r.json().get('url')}")
                            else:
                                st.error(f"❌ Błąd '{uploaded.name}': {r.status_code} — {r.text[:200]}")
