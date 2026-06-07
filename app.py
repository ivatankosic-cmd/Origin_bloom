import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

# Podešavanje cele stranice na "Wide" (opciono, ali daje više prostora) i sakrivanje default menija
st.set_page_config(page_title="Origin Bloom", page_icon="🌸", layout="centered")

# PREMIUM CSS STILIZACIJA
st.markdown("""
    <style>
    /* Uvoz luksuznih fontova sa Google-a */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Montserrat:wght@300;400;500&display=swap');

    /* Sakrivanje Streamlit menija i footera za čistiji izgled */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glavni fontovi */
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        color: #333333;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #1a1a1a;
        font-weight: 600;
    }

    /* Stilizacija unosa (polja) - elegantne tanke linije umesto debelih okvira */
    div[data-baseweb="input"] { 
        border: none !important;
        border-bottom: 1px solid #dcdcdc !important; 
        border-radius: 0px !important;
        background-color: transparent !important;
    }
    div[data-baseweb="input"]:focus-within { 
        border-bottom: 1px solid #a8c69f !important; 
    }
    
    /* Brending i naslovi */
    .brand-name { 
        font-size: 14px; 
        color: #888; 
        letter-spacing: 3px; 
        text-transform: uppercase; 
        text-align: center;
        margin-bottom: -10px;
    }
    .main-title {
        text-align: center;
        font-size: 42px !important;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        font-style: italic;
        color: #666;
        margin-bottom: 40px;
    }

    /* Sekcija sa rezultatima */
    .result-section {
        background-color: #fbfbf9; /* Vrlo blaga topla siva/bež za premium osećaj */
        padding: 40px 30px;
        border-radius: 2px;
        border: 1px solid #eaeaea;
        margin-top: 30px;
    }
    
    .result-title { font-size: 24px; text-align: center; margin-bottom: 5px; }
    .result-subtitle { font-size: 15px; text-align: center; color: #555; margin-bottom: 30px; }
    
    .planet-row {
        font-size: 16px;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .sun-message { 
        font-family: 'Playfair Display', serif;
        font-size: 18px; 
        font-style: italic; 
        text-align: center; 
        color: #444; 
        margin-top: 35px; 
        margin-bottom: 15px;
    }
    
    .note-text {
        font-size: 13px;
        color: #777;
        text-align: center;
        line-height: 1.6;
        margin-top: 20px;
        padding: 0 20px;
    }

    /* Umetnički proces sekcija */
    .art-process {
        margin-top: 50px;
        padding: 0 20px;
    }
    .process-title {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .process-text {
        font-size: 15px;
        line-height: 1.8;
        color: #444;
        text-align: justify;
    }

    /* Dugme */
    .stButton>button {
        width: 100%;
        background-color: #2c3e2e !important; /* Tamno, elegantno zelena */
        color: white !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
        letter-spacing: 1px;
        padding: 12px;
        border-radius: 0px;
        border: none;
        margin-top: 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #425c45 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Origin Bloom</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>buket koji te opisuje</p>", unsafe_allow_html=True)

def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

try:
    xls = load_excel()
except Exception as e:
    st.error("Excel fajl nije pronađen.")
    st.stop()

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

# Polja za unos
col_lok1, col_lok2 = st.columns(2)
drzava = col_lok1.text_input("Država rođenja")
grad = col_lok2.text_input("Grad rođenja")

st.write("") # Prazan prostor
st.markdown("**Datum rođenja**")
col_dan, col_mesec, col_godina = st.columns(3)
dan = col_dan.number_input("Dan", min_value=1, max_value=31, value=1)
mesec = col_mesec.number_input("Mesec", min_value=1, max_value=12, value=1)
godina = col_godina.number_input("Godina", min_value=1900, max_value=2026, value=1990)

st.write("")
st.markdown("**Vreme rođenja**")
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
            
            # SEKCIJA 1: Prikaz rezultata (Premium kontejner)
            st.markdown(f"""
            <div class='result-section'>
                <h2 class='result-title'>Tvoj Origin Bloom profil je kreiran.</h2>
                <p class='result-subtitle'>Precizni podaci prevedeni su u tvoj jedinstveni botanički i koloritni potpis.</p>
                <div style='text-align: center; margin-bottom: 20px; font-weight: 500;'>
                    Znak: {znak_ime} &nbsp;|&nbsp; Podznak: {podznak_ime}
                </div>
            """, unsafe_allow_html=True)
            
            sve_planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars'}
            poruka_sunce = "" 
            
            # Ispis planeta
            for id, ime in sve_planete.items():
                pos = swe.calc_ut(jd, id)[0][0]
                znak = ZNACI[int(pos // 30)]
                sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
                if sheet:
                    df = pd.read_excel(xls, sheet_name=sheet, header=2)
                    df.columns = df.columns.str.strip()
                    match = df[df['Znak'] == znak]
                    if not match.empty:
                        st.markdown(f"<div class='planet-row'><b>{ime} ({znak}):</b> {match.iloc[0]['Biljka']} | <i>{match.iloc[0]['Boja']}</i></div>", unsafe_allow_html=True)
                        
                        if id == 0 and 'Poruka' in match.columns:
                            poruka_sunce = match.iloc[0]['Poruka']
            
            # Poruka za Sunce i Napomena
            if poruka_sunce:
                st.markdown(f"<div class='sun-message'>✨ {poruka_sunce}</div>", unsafe_allow_html=True)
            
            st.markdown("<p class='note-text'>Ovo je sirovi materijal tvog identiteta. Iako ove boje i oblici na prvi pogled možda deluju nespojivo, njihov pravi estetski potencijal otkriva se tek kroz umetničku sintezu.</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True) # Kraj result-section
            
            # SEKCIJA 2: Umetnički proces i očekivanja
            st.markdown("""
            <div class='art-process'>
                <h3 class='process-title'>Od koda do kompozicije</h3>
                <p class='process-text'>Ovde se završava proračun i počinje umetnost. Na osnovu tvog koda, ručno osmišljavam kompoziciju, tražim savršen balans između dodeljenih nijansi i oblika. Kroz igru odnosa figure i pozadine, svaki element dobija svoj prostor, gradeći harmoničnu celinu.</p>
                
                <h3 class='process-title'>Vreme izrade</h3>
                <p class='process-text'>Proces kreiranja ovakvog dela zahteva vreme, mir i slojevitu izgradnju akvarela uz korišćenje premium papira i specifičnih tehnika. Zbog mog posvećenog pristupa svakom unikatnom delu, rok za izradu tvog personalizovanog Origin Bloom originala je 3 nedelje.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.markdown("<p class='cta-text'><b>Origin Bloom</b> je premium, personalizovana slika, ručno crtana na osnovu tvoje natalne karte.<br>Naručite vašu sliku na našoj Instagram strani.</p>", unsafe_allow_html=True)
            st.link_button("🌸 Naruči svoju sliku na Instagramu", "https://instagram.com/etherealbyiva", use_container_width=True)
            
        except ValueError:
            st.error("Uneti datum ne postoji (proveri broj dana u mesecu).")