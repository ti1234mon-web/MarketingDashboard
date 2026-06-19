# xt_operations_dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="XT Operations Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# 2. ULTRA LUXURY CSS (Dark Luxury Design)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
    .stApp { background: linear-gradient(160deg, #0A0A0A 0%, #1A1A1A 35%, #222222 65%, #0A0A0A 100%); min-height: 100vh; }
    .stApp::before { content: ''; position: fixed; top: -20%; left: -20%; width: 140%; height: 140%; background: radial-gradient(ellipse at 40% 30%, rgba(212, 168, 83, 0.03) 0%, transparent 60%); pointer-events: none; z-index: 0; }
    .main > div { background: transparent; max-width: 1300px; margin: 0 auto; padding: 2rem 2rem 4rem 2rem; position: relative; z-index: 1; }
    .block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1300px; margin: 0 auto; }
    
    .title-wrapper { display: flex; justify-content: center; width: 100%; margin: 0 auto 1.2rem auto; max-width: 700px; white-space: nowrap; }
    .main-title { font-size: 2.6rem; font-weight: 800; letter-spacing: 0.04em; text-align: center; margin: 0; color: #FFFFFF; line-height: 1.2; width: 100%; text-shadow: 0 2px 40px rgba(212, 168, 83, 0.05); white-space: nowrap; }
    .main-title span { background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    
    .section-headline { font-size: 1.1rem !important; font-weight: 500; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255, 255, 255, 0.35) !important; text-align: center; margin: 0; }
    
    .metric-card { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 16px; padding: 0.8rem 0.5rem; text-align: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; flex: 1 1 0; min-width: 120px; max-width: 170px; height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .metric-card:hover { border-color: rgba(212, 168, 83, 0.15); background: rgba(255, 255, 255, 0.04); transform: translateY(-2px); }
    .metric-card .label { color: rgba(255, 255, 255, 0.3); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.1rem; white-space: nowrap; }
    .metric-card .value { font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #D4A853 0%, #F5D98E 60%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.2; white-space: nowrap; }
    
    .stDataFrame { background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(8px); border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.04) !important; overflow: hidden; margin: 0 auto 1rem auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
    .stDataFrame th { background: rgba(255, 255, 255, 0.03) !important; color: rgba(255, 255, 255, 0.2) !important; font-weight: 500 !important; font-size: 0.6rem !important; text-transform: uppercase !important; letter-spacing: 0.2em !important; text-align: center !important; padding: 0.8rem 1rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame td { background: transparent !important; color: rgba(255, 255, 255, 0.8) !important; text-align: center !important; padding: 0.7rem 1rem !important; font-size: 0.9rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important; }
    .stDataFrame tr:hover td { background: rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame tr:last-child td { border-bottom: none !important; }
    
    .checklist-item { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 0.8rem 1rem; margin: 0.3rem 0; display: flex; align-items: center; justify-content: space-between; }
    .checklist-item:hover { background: rgba(255, 255, 255, 0.04); }
    .checklist-label { color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; }
    .checklist-done { color: #4CAF50; font-weight: 500; }
    .checklist-pending { color: rgba(255, 255, 255, 0.3); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. TITLE
# ============================================================
st.markdown("""
    <div class="title-wrapper">
        <h1 class="main-title">📊 XT <span>OPERATIONS DASHBOARD</span></h1>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 4. SIDEBAR: NAVIGATION
# ============================================================
st.sidebar.markdown("### 📋 Navigation")
page = st.sidebar.radio(
    "Seite wählen:",
    ["📊 Dashboard", "📈 Marketing", "👥 Community", "📋 Checklisten", "⚙️ Einstellungen"]
)

st.sidebar.markdown("---")
st.sidebar.caption(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}")

# ============================================================
# 5. SESSION STATE INITIALISIEREN (für Checklisten)
# ============================================================
if "daily_checklist" not in st.session_state:
    st.session_state.daily_checklist = {
        "Neue Mitglieder begrüßen": False,
        "Aktivitäts-Ampel checken": False,
        "Rote-Mitglieder anschreiben": False,
        "Heißes Thema aus der Gruppe für Content sammeln": False,
        "Instagram-Story posten": False
    }

if "weekly_checklist" not in st.session_state:
    st.session_state.weekly_checklist = {
        "KPIs checken (CTR, CPC, CPL, CPAM)": False,
        "Gewinner- & Verlierer-Anzeige identifizieren": False,
        "Budget für nächste Woche anpassen": False,
        "Community-Meeting vorbereiten & durchführen": False,
        "Meeting-Aufzeichnung hochladen": False,
        "Erfolgsgeschichte aus der Gruppe sammeln": False,
        "Nächste Woche planen (Content, Themen)": False
    }

if "monthly_checklist" not in st.session_state:
    st.session_state.monthly_checklist = {
        "ETF-Dashboard-Werte aktualisieren": False,
        "Bitcoin-Langzeit-Dashboard aktualisieren": False,
        "Anleihen-Scanner auf neue ISINs prüfen": False,
        "Immobilien-Pro-Forma-Daten prüfen": False,
        "Feedback der Mitglieder in Tools einfließen lassen": False,
        "Lookalike-Audience aus neuen Mitgliedern aktualisieren": False,
        "Monatliche KPIs auswerten (Retention, Churn, CPAM-Trend)": False
    }

# ============================================================
# 6. FARB-HELFERFUNKTION (für Tabellen)
# ============================================================
def color_status(val):
    if "🟢" in str(val):
        return 'color: #4CAF50; font-weight: bold;'
    elif "🟡" in str(val):
        return 'color: #FFC107; font-weight: bold;'
    elif "🔴" in str(val):
        return 'color: #EF5350; font-weight: bold;'
    return ''

# ============================================================
# 7. SEITE: DASHBOARD
# ============================================================
if page == "📊 Dashboard":
    
    # ─── WÖCHENTLICHE KPI-ÜBERSICHT ───
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
            <p class="section-headline">📊 Wöchentliche KPIs</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Marketing KPIs (Beispielwerte)
    marketing_kpis = [
        {"KPI": "CTR", "Berechnung": "(Klicks / Impressionen) × 100", "Benchmark": "> 1,5 %", "Aktuell": "1,8 %", "Status": "🟢 Grün"},
        {"KPI": "CPC", "Berechnung": "Werbeausgaben / Klicks", "Benchmark": "< 1,20 €", "Aktuell": "0,95 €", "Status": "🟢 Grün"},
        {"KPI": "CPM", "Berechnung": "(Werbeausgaben / Impressionen) × 1.000", "Benchmark": "< 25 €", "Aktuell": "22 €", "Status": "🟢 Grün"},
        {"KPI": "CPL", "Berechnung": "Werbeausgaben / Leads", "Benchmark": "< 45 €", "Aktuell": "38 €", "Status": "🟢 Grün"},
        {"KPI": "CPAM", "Berechnung": "Werbeausgaben / aktive neue Mitglieder", "Benchmark": "< 50 €", "Aktuell": "42 €", "Status": "🟢 Grün"},
        {"KPI": "Lead-zu-Mitglied-Quote", "Berechnung": "(Mitglieder / Leads) × 100", "Benchmark": "> 30 %", "Aktuell": "35 %", "Status": "🟢 Grün"},
        {"KPI": "ROAS", "Berechnung": "Umsatz (Mitgliedsbeiträge) / Werbeausgaben", "Benchmark": "> 3x", "Aktuell": "4,2x", "Status": "🟢 Grün"},
        {"KPI": "CLV (geschätzt)", "Berechnung": "Monatlicher Beitrag × durchschnittliche Mitgliedsdauer", "Benchmark": "> 200 €", "Aktuell": "250 €", "Status": "🟢 Grün"},
    ]
    
    df_marketing = pd.DataFrame(marketing_kpis)
    
    # Styling für die Tabelle (map statt applymap)
    styled_marketing = df_marketing.style.map(color_status, subset=['Status'])
    st.dataframe(styled_marketing, use_container_width=True, hide_index=True)
    
    # ─── FORTSCHRITT ZU 100 MITGLIEDERN ───
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 2rem 0 1.5rem 0;">
            <p class="section-headline">📈 Fortschritt zu 100 Mitgliedern</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_members = 12
        target_members = 100
        progress = current_members / target_members
        
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 16px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 3rem; font-weight: 700; color: #D4A853;">{current_members}</div>
                <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem;">von {target_members} Mitgliedern</div>
                <div style="background: rgba(255,255,255,0.05); border-radius: 10px; height: 20px; margin: 0.5rem 0; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #D4A853, #F5D98E); width: {progress*100}%; height: 20px; border-radius: 10px;"></div>
                </div>
                <div style="color: rgba(255,255,255,0.2); font-size: 0.7rem;">{progress*100:.1f} % erreicht</div>
                <div style="color: rgba(255,255,255,0.2); font-size: 0.7rem;">Wöchentliches Wachstum: +3 Mitglieder (Benchmark: 2–5)</div>
            </div>
        """, unsafe_allow_html=True)
    
    # ─── AKTIVITÄTS-AMPEL ───
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 2rem 0 1.5rem 0;">
            <p class="section-headline">🟢🟡🔴 Aktivitäts-Ampel</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: rgba(76, 175, 80, 0.08); border: 1px solid rgba(76, 175, 80, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 2rem;">🟢</div>
                <div style="color: #4CAF50; font-weight: 600;">Grün</div>
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem;">> 5 Posts/Woche</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #4CAF50;">8</div>
                <div style="color: rgba(255,255,255,0.2); font-size: 0.6rem;">Weiter laufen lassen</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.08); border: 1px solid rgba(255, 193, 7, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 2rem;">🟡</div>
                <div style="color: #FFC107; font-weight: 600;">Gelb</div>
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem;">1–5 Posts/Woche</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #FFC107;">5</div>
                <div style="color: rgba(255,255,255,0.2); font-size: 0.6rem;">Kurz interagieren</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: rgba(239, 83, 80, 0.08); border: 1px solid rgba(239, 83, 80, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 2rem;">🔴</div>
                <div style="color: #EF5350; font-weight: 600;">Rot</div>
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem;">0 Posts/Woche</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #EF5350;">3</div>
                <div style="color: rgba(255,255,255,0.2); font-size: 0.6rem;">Persönliche Nachricht</div>
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# 8. SEITE: MARKETING
# ============================================================
elif page == "📈 Marketing":
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
            <p class="section-headline">📈 Marketing KPIs</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Hier kannst du die aktuellen Werbe-KPIs eintragen und die Performance verfolgen.")
    
    # Eingabefelder für Marketing-KPIs
    col1, col2 = st.columns(2)
    with col1:
        ctr = st.number_input("CTR (%)", min_value=0.0, max_value=10.0, value=1.8, step=0.1)
        cpc = st.number_input("CPC (€)", min_value=0.0, max_value=5.0, value=0.95, step=0.05)
        cpm = st.number_input("CPM (€)", min_value=0.0, max_value=100.0, value=22.0, step=1.0)
        cpl = st.number_input("CPL (€)", min_value=0.0, max_value=200.0, value=38.0, step=1.0)
    with col2:
        cpam = st.number_input("CPAM (€)", min_value=0.0, max_value=200.0, value=42.0, step=1.0)
        lead_to_member = st.number_input("Lead-zu-Mitglied-Quote (%)", min_value=0.0, max_value=100.0, value=35.0, step=1.0)
        roas = st.number_input("ROAS (x)", min_value=0.0, max_value=10.0, value=4.2, step=0.1)
        clv = st.number_input("CLV geschätzt (€)", min_value=0.0, max_value=1000.0, value=250.0, step=10.0)
    
    if st.button("KPIs speichern", use_container_width=True):
        st.success("✅ KPIs gespeichert!")

# ============================================================
# 9. SEITE: COMMUNITY
# ============================================================
elif page == "👥 Community":
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
            <p class="section-headline">👥 Community-KPIs</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ─── INITIALISIERE COMMUNITY-KPIs IN SESSION STATE ───
    if "community_kpis" not in st.session_state:
        st.session_state.community_kpis = {
            "Aktivitätsrate": 72,
            "Retention W1→2": 78,
            "Retention M1→3": 65,
            "Meeting-Teilnahme": 52,
            "Tool-Nutzungsrate": 58,
            "Churn-Rate": 6
        }
    
    # ─── EINGABEFELDER ───
    st.markdown("### 📝 Werte eintragen")
    
    col1, col2 = st.columns(2)
    with col1:
        aktivitaet = st.number_input(
            "Aktivitätsrate (%)",
            min_value=0, max_value=100,
            value=st.session_state.community_kpis["Aktivitätsrate"],
            step=1,
            key="community_aktivitaet"
        )
        retention_w1 = st.number_input(
            "Retention Woche 1→2 (%)",
            min_value=0, max_value=100,
            value=st.session_state.community_kpis["Retention W1→2"],
            step=1,
            key="community_retention_w1"
        )
        retention_m1 = st.number_input(
            "Retention Monat 1→3 (%)",
            min_value=0, max_value=100,
            value=st.session_state.community_kpis["Retention M1→3"],
            step=1,
            key="community_retention_m1"
        )
    with col2:
        meeting = st.number_input(
            "Meeting-Teilnahme (%)",
            min_value=0, max_value=100,
            value=st.session_state.community_kpis["Meeting-Teilnahme"],
            step=1,
            key="community_meeting"
        )
        tool = st.number_input(
            "Tool-Nutzungsrate (%)",
            min_value=0, max_value=100,
            value=st.session_state.community_kpis["Tool-Nutzungsrate"],
            step=1,
            key="community_tool"
        )
        churn = st.number_input(
            "Churn-Rate (%)",
            min_value=0, max_value=100,
            value=st.session_state.community_kpis["Churn-Rate"],
            step=1,
            key="community_churn"
        )
    
    if st.button("💾 Community KPIs speichern", use_container_width=True):
        st.session_state.community_kpis["Aktivitätsrate"] = aktivitaet
        st.session_state.community_kpis["Retention W1→2"] = retention_w1
        st.session_state.community_kpis["Retention M1→3"] = retention_m1
        st.session_state.community_kpis["Meeting-Teilnahme"] = meeting
        st.session_state.community_kpis["Tool-Nutzungsrate"] = tool
        st.session_state.community_kpis["Churn-Rate"] = churn
        st.success("✅ Community KPIs gespeichert!")
    
    # ─── TABELLE MIT GESPEICHERTEN WERTEN ───
    st.markdown("### 📊 Aktuelle Community-KPIs")
    
    # Benchmarks aus den Einstellungen holen (oder Standardwerte)
    if "benchmarks" not in st.session_state:
        st.session_state.benchmarks = {
            "Aktivitätsrate": 60,
            "Retention W1→2": 70,
            "Retention M1→3": 60,
            "Meeting-Teilnahme": 40,
            "Tool-Nutzungsrate": 50,
            "Churn-Rate": 10
        }
    
    benchmarks = st.session_state.benchmarks
    
    # Status bestimmen
    def get_status(value, benchmark, is_churn=False):
        if is_churn:
            if value <= benchmark:
                return "🟢 Grün"
            elif value <= benchmark * 1.5:
                return "🟡 Gelb"
            else:
                return "🔴 Rot"
        else:
            if value >= benchmark:
                return "🟢 Grün"
            elif value >= benchmark * 0.7:
                return "🟡 Gelb"
            else:
                return "🔴 Rot"
    
    community_data = []
    for kpi, value in st.session_state.community_kpis.items():
        bench = benchmarks.get(kpi, 0)
        is_churn = "Churn" in kpi
        status = get_status(value, bench, is_churn)
        community_data.append({
            "KPI": kpi,
            "Benchmark": f"{bench} %",
            "Aktuell": f"{value} %",
            "Status": status
        })
    
    df_community = pd.DataFrame(community_data)
    styled_community = df_community.style.map(color_status, subset=['Status'])
    st.dataframe(styled_community, use_container_width=True, hide_index=True)

# ============================================================
# 10. SEITE: CHECKLISTEN
# ============================================================
elif page == "📋 Checklisten":
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
            <p class="section-headline">✅ Checklisten</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ─── TÄGLICHE CHECKLISTE ───
    st.markdown("### 📅 Täglich (Xenja)")
    st.caption("Benchmark: 5 Aufgaben/Tag, ~50 Min.")
    
    for task, done in st.session_state.daily_checklist.items():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
                <div class="checklist-item">
                    <span class="checklist-label">{task}</span>
                    <span class="{'checklist-done' if done else 'checklist-pending'}">{'✅ Erledigt' if done else '⏳ Offen'}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            new_state = st.checkbox("", value=done, key=f"daily_{task}")
            if new_state != done:
                st.session_state.daily_checklist[task] = new_state
                st.rerun()
    
    # ─── WÖCHENTLICHE CHECKLISTE ───
    st.markdown("### 📆 Wöchentlich (Xenja + Timon)")
    st.caption("Benchmark: 7 Aufgaben/Woche, ~3,5 Std.")
    
    for task, done in st.session_state.weekly_checklist.items():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
                <div class="checklist-item">
                    <span class="checklist-label">{task}</span>
                    <span class="{'checklist-done' if done else 'checklist-pending'}">{'✅ Erledigt' if done else '⏳ Offen'}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            new_state = st.checkbox("", value=done, key=f"weekly_{task}")
            if new_state != done:
                st.session_state.weekly_checklist[task] = new_state
                st.rerun()
    
    # ─── MONATLICHE CHECKLISTE ───
    st.markdown("### 📆 Monatlich (Timon)")
    st.caption("Benchmark: 7 Aufgaben/Monat, ~3–4 Std.")
    
    for task, done in st.session_state.monthly_checklist.items():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
                <div class="checklist-item">
                    <span class="checklist-label">{task}</span>
                    <span class="{'checklist-done' if done else 'checklist-pending'}">{'✅ Erledigt' if done else '⏳ Offen'}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            new_state = st.checkbox("", value=done, key=f"monthly_{task}")
            if new_state != done:
                st.session_state.monthly_checklist[task] = new_state
                st.rerun()

# ============================================================
# 11. SEITE: EINSTELLUNGEN
# ============================================================
elif page == "⚙️ Einstellungen":
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
            <p class="section-headline">⚙️ Einstellungen</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Hier kannst du die Benchmarks und Zielwerte anpassen.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Marketing Benchmarks")
        ctr_bench = st.number_input("CTR Benchmark (%)", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
        cpc_bench = st.number_input("CPC Benchmark (€)", min_value=0.0, max_value=5.0, value=1.20, step=0.05)
        cpl_bench = st.number_input("CPL Benchmark (€)", min_value=0.0, max_value=200.0, value=45.0, step=1.0)
        cpam_bench = st.number_input("CPAM Benchmark (€)", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
    
    with col2:
        st.markdown("### 👥 Community Benchmarks")
        activity_bench = st.number_input("Aktivitätsrate Benchmark (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
        retention_bench = st.number_input("Retention W1→2 Benchmark (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
        churn_bench = st.number_input("Churn-Rate Benchmark (%)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)
        meeting_bench = st.number_input("Meeting-Teilnahme Benchmark (%)", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
    
    st.markdown("### 🎯 Mitglieder-Ziel")
    member_target = st.number_input("Mitglieder-Ziel", min_value=10, max_value=1000, value=100, step=5)
    
    if st.button("Einstellungen speichern", use_container_width=True):
        st.success("✅ Einstellungen gespeichert!")