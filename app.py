import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

st.set_page_config(page_title="Origin Bloom", page_icon="🌸", layout="centered")

# ULTRA-PREMIUM CSS STILIZACIJA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Topla pozadina nalik luksuznom papiru */
    .stApp {
        background-color: #FAF9F6; 
    }

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        color: #2c2c2c;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #111111;
        font-weight: 500;
    }

    /* Stilizacija labela iznad polja za unos */
    label, .st-emotion-cache-1y0t1k8, .st-emotion-cache-1jbcvrx {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #888888 !important;
        font-weight: 400 !important;
        padding-bottom: 5px;
    }

    div[data-baseweb="input"] { 
        border: none !important;
        border-bottom: 1px solid #e5e5e5 !important; 
        border-radius: 0px !important;
        background-color: transparent !important;
    }
    div[data-baseweb="input"]:focus-within { 
        border-bottom: 1px solid #B89768 !important; 
    }
    
    /* BRAND NAME I NASLOVI */
    .brand-name { 
        font-size: 12px; 
        color: #B89768; 
        letter-spacing: 4px; 
        text-transform: uppercase; 
        text-align: center;
        margin-bottom: 5px;
        font-weight: 500;
    }
    .main-title {
        text-align: center;
        font-size: 46px !important;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sub-title {
        text-align: center;
        font-size: 16px;
        font-family: 'Playfair Display', serif;
        font-style: italic;
        color: #777;
        margin-bottom: 15px;
    }
    .gold-divider {
        width: 40px;
        height: 1px;
        background-color: #B89768;
        margin: 0px auto 40px auto;
    }

    /* Sekcija sa rezultatima - oštre ivice, suptilna senka */
    .result-section {
        background-color: #ffffff; 
        padding: 50px 40px;
        border-radius: 0px;
        border: 1px solid #f2f2f2;
        margin-top: 40px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.02); 
    }
    
    .result-title { font-size: 26px; text-align: center; margin-bottom: 10px; }
    .result-subtitle { font-size: 14px; text-align: center; color: #666; margin-bottom: 40px; line-height: 1.6; }
    
    .astrology-header {
        text-align: center;
        margin-bottom: 30px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #888;
    }

    .planet-row {
        font-size: 15px;
        padding: 12px 0;
        border-bottom: 1px solid #f9f9f9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .planet-name {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #999;
        font-weight: 500;
    }
    .planet-result {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 17px;
        color: #222;
        text-align: right;
    }
    
    .sun-message { 
        font-family: 'Playfair Display', serif;
        font-size: 19px; 
        font-style: italic; 
        text-align: center; 
        color: #B89768; 
        margin-top: 45px; 
        margin-bottom: 25px;
        line-height: 1.5;
    }
    
    .note-text {
        font-size: 11px;
        color: #a0a0a0;
        text-align: center;
        line-height: 1.8;
        margin-top: 35px;
        padding: 0 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Umetnički proces sekcija */
    .art-process {
        margin-top: 60px;
        padding: 0 20px;
    }
    .process-title {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 15px;
        color: #222;
    }
    .process-text {
        font-size: 14px;
        line-height: 2;
        color: #555;
        text-align: center;
        font-weight: 300;
    }

    /* Standardno dugme (Prikaži potpis) */
    .stButton > button {
        width: 100%;
        background-color: transparent !important;
        color: #2c3e2e !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 15px;
        border-radius: 0px;
        border: 1px solid #2c3e2e !important;
        margin-top: 30px;
        transition: all 0.4s ease;
    }
    .stButton > button:hover {
        background-color: #2c3e2e !important;
        color: white !important;
    }
    
    /* CTA Kontejner - Izdvojen blok za naručivanje */
    .cta-container {
        text-align: center; 
        padding: 35px 30px; 
        margin-top: 50px; 
        margin-bottom: 10px; 
        background-color: #f4f1ea; 
        border: 1px solid #e8e2d5;
        font-size: 14px; 
        color: #444; 
        line-height: 1.8;
        font-weight: 400;
    }

    /* Dugme za Instagram (Link Button) */
    .stLinkButton > a {
        width: 100%;
        background-color: #2c3e2e !important;
        color: #ffffff !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 15px;
        border-radius: 0px;
        border: none !important;
        margin-top: 10px;
        margin-bottom: 40px;
        transition: all 0.4s ease;
        box-shadow: 0px 5px 15px rgba(44, 62, 46, 0.2);
        display: inline-block;
        text-align: center;
        text-decoration: none;
    }
    .stLinkButton > a:hover {
        background-color: #B89768 !important;
        color: white !important;
        box-shadow: 0px 5px 15px rgba(184, 151, 104, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Origin Bloom</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>buket koji te opisuje</p>", unsafe_allow_html=True)
st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

try:
    xls = load_excel()
except Exception as e:
    st.error("Excel fajl nije pronađen.")
    st.stop()

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

col_lok1, col_lok2 = st.columns(2)
drzava = col_lok1.text_input("Država rođenja")
grad = col_lok2.text_input("Grad rođenja")

st.write("") 
st.markdown("<div style='margin-bottom: -15px;'><label>Datum rođenja</label></div>", unsafe_allow_html=True)
col_dan, col_mesec, col_godina = st.columns(3)
dan = col_dan.number_input("Dan", min_value=1, max_value=31, value=1)
mesec = col_mesec.number_input("Mesec", min_value=1, max_value=12, value=1)
godina = col_godina.number_input("Godina", min_value=1900, max_value=2026, value=1990)

st.write("")
st.markdown("<div style='margin-bottom: -15px;'><label>Vreme rođenja</label></div>", unsafe_allow_html=True)
col_sat, col_min = st.columns(2)
sati = col_sat.number_input("Sati", 0, 23, 12)
minuti = col_min.number_input("Minuti", 0, 59, 0)

if st.button("Prikaži moj potpis"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    location = geolocator.geocode(f"{grad}, {drzava}")
    
    if not location:
        st.error("Nisam pronašao lokaciju. Proveri unos.")
    else:
        try:
            tf = TimezoneFinder()
            tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
            if tz_str is None: tz_str = "UTC"
                
            local_tz = pytz.timezone(tz_str)
            lokalno_vreme = datetime(int(godina), int(mesec), int(dan), int(sati), int(minuti))
            
            try:
                lokalno_vreme_sa_zonom = local_tz.localize(lokalno_vreme, is_dst=None)
            except (pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
                lokalno_vreme_sa_zonom = local_tz.localize(lokalno_vreme, is_dst=False)
                
            utc_vreme = lokalno_vreme_sa_zonom.astimezone(pytz.utc)
            jd = swe.julday(utc_vreme.year, utc_vreme.month, utc_vreme.day, utc_vreme.hour + utc_vreme.minute/60.0)
            
            pos_sunce = swe.calc_ut(jd, 0)[0][0]
            znak_ime = ZNACI[int(pos_sunce // 30)]
            cusps, ascmc = swe.houses(jd, location.latitude, location.longitude, b'P')
            podznak_ime = ZNACI[int(ascmc[0] // 30)]
            
            # ISPRAVLJENO: Nema više praznih redova u HTML bloku!
            st.markdown(f"""<div class='result-section'>
                <h2 class='result-title'>Tvoj Origin Bloom profil je kreiran.</h2>
                <p class='result-subtitle'>Precizni podaci prevedeni su u tvoj jedinstveni botanički i koloritni potpis.</p>
                <div class='astrology-header'>Znak: <b>{znak_ime}</b> &nbsp;|&nbsp; Podznak: <b>{podznak_ime}</b></div>
            """, unsafe_allow_html=True)
            
            sve_planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars'}
            poruka_sunce = "" 
            
            for id, ime in sve_planete.items():
                pos = swe.calc_ut(jd, id)[0][0]
                znak = ZNACI[int(pos // 30)]
                sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
                if sheet:
                    df = pd.read_excel(xls, sheet_name=sheet, header=2)
                    df.columns = df.columns.str.strip()
                    match = df[df['Znak'] == znak]
                    if not match.empty:
                        st.markdown(f"""<div class='planet-row'><span class='planet-name'>{ime} ({znak})</span><span class='planet-result'>{match.iloc[0]['Biljka']} | <span style='color:#B89768;'>{match.iloc[0]['Boja']}</span></span></div>""", unsafe_allow_html=True)
                        
                        if id == 0 and 'Poruka' in match.columns:
                            poruka_sunce = match.iloc[0]['Poruka']
            
            if poruka_sunce:
                st.markdown(f"<div class='sun-message'>✨ {poruka_sunce}</div>", unsafe_allow_html=True)
            
            st.markdown("<p class='note-text'>Ovo je sirovi materijal tvog identiteta.<br>Iako ove boje i oblici na prvi pogled možda deluju nespojivo, njihov pravi estetski potencijal otkriva se tek kroz umetničku sintezu.</p></div>", unsafe_allow_html=True)
            
            # ISPRAVLJENO: Nema više praznih redova u HTML bloku!
            st.markdown("""<div class='art-process'>
                <h3 class='process-title'>Od koda do kompozicije</h3>
                <p class='process-text'>Ovde se završava proračun i počinje umetnost. Na osnovu tvog koda, ručno osmišljavam kompoziciju, tražim savršen balans između dodeljenih nijansi i oblika. Kroz igru odnosa figure i pozadine, svaki element dobija svoj prostor, gradeći harmoničnu celinu.</p>
                <h3 class='process-title'>Vreme izrade</h3>
                <p class='process-text'>Proces kreiranja ovakvog dela zahteva vreme, mir i slojevitu izgradnju akvarela uz korišćenje premium papira i specifičnih tehnika. Zbog mog posvećenog pristupa svakom unikatnom delu, rok za izradu tvog personalizovanog Origin Bloom originala je 3 nedelje.</p>
            </div>""", unsafe_allow_html=True)
            
            st.markdown("<div class='cta-container'><b>Origin Bloom</b> je premium, personalizovana slika, ručno crtana na osnovu tvoje natalne karte.<br><br>Naručite vašu sliku na našoj Instagram strani.</div>", unsafe_allow_html=True)
            
            st.link_button("🌸 Naruči svoju sliku na Instagramu", "https://instagram.com/etherealbyiva", use_container_width=True)
            
        except ValueError:
            st.error("Uneti datum ne postoji (proveri broj dana u mesecu).")