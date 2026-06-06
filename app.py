import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import pytz

# Stil za zelene okvire
st.markdown("""
    <style>
    div[data-baseweb="input"] { border: 2px solid #A8C69F !important; }
    div[data-baseweb="input"]:focus-within { border: 2px solid #4CAF50 !important; }
    h1 { font-size: 28px !important; }
    .brand-name { font-size: 16px; color: #777; letter-spacing: 2px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.title("🌸Origin Bloom")
st.subheader("buket koji te opisuje")

def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

xls = load_excel()
ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

drzava = st.text_input("Država rođenja")
grad = st.text_input("Grad rođenja")

st.write("**Datum rođenja**")
col_dan, col_mesec, col_godina = st.columns(3)
dan = col_dan.number_input("Dan", min_value=1, max_value=31, value=9)
mesec = col_mesec.number_input("Mesec", min_value=1, max_value=12, value=4)
godina = col_godina.number_input("Godina", min_value=1900, max_value=2026, value=1988)

st.write("**Vreme rođenja**")
col_sat, col_min = st.columns(2)
sati = col_sat.number_input("Sati", 0, 23, 12)
minuti = col_min.number_input("Minuti", 0, 59, 0)

if st.button("prikaži moje cveće"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    location = geolocator.geocode(f"{grad}, {drzava}")
    
    if not location:
        st.error("Nisam pronašao lokaciju. Proveri unos.")
    else:
        try:
            lokalno_vreme = datetime(int(godina), int(mesec), int(dan), int(sati), int(minuti))
            
            # PAMETNA DETEKCIJA ZA BALKAN (Zaobilazi greške u svetskim bazama za 80-te)
            balkan_drzave = ['srbija', 'serbia', 'hrvatska', 'croatia', 'bosna', 'bosnia', 'crna gora', 'montenegro', 'makedonija', 'macedonia', 'slovenija', 'slovenia']
            is_balkan = any(zemlja in drzava.lower() for zemlja in balkan_drzave)
            
            if is_balkan:
                offset = 1 # Standardno zimsko vreme (GMT+1)
                if godina >= 1983:
                    # Letnje vreme na Balkanu (GMT+2)
                    if 4 <= mesec <= 9:
                        offset = 2
                    elif mesec == 3 and dan >= 25:
                        offset = 2
                    elif mesec == 10 and dan <= 25:
                        offset = 2
                utc_vreme = lokalno_vreme - timedelta(hours=offset)
            else:
                # Za ostatak sveta koristi globalnu mapu
                tf = TimezoneFinder()
                tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
                if tz_str is None: tz_str = "UTC"
                local_tz = pytz.timezone(tz_str)
                try:
                    utc_vreme = local_tz.localize(lokalno_vreme, is_dst=None).astimezone(pytz.utc)
                except (pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
                    utc_vreme = local_tz.localize(lokalno_vreme, is_dst=False).astimezone(pytz.utc)

            # Astrološka kalkulacija sa tačnim UTC vremenom
            jd = swe.julday(utc_vreme.year, utc_vreme.month, utc_vreme.day, utc_vreme.hour + utc_vreme.minute/60.0)
            
            pos_sunce = swe.calc_ut(jd, 0)[0][0]
            znak_ime = ZNACI[int(pos_sunce // 30)]
            cusps, ascmc = swe.houses(jd, location.latitude, location.longitude, b'P')
            podznak_ime = ZNACI[int(ascmc[0] // 30)]
            
            st.success("### Tvoj lični pečat")
            st.write(f"**Znak:** {znak_ime} | **Podznak:** {podznak_ime}")
            st.divider()
            
            # Prikaz 5 planeta
            sve_planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars'}
            for id, ime in sve_planete.items():
                pos = swe.calc_ut(jd, id)[0][0]
                znak = ZNACI[int(pos // 30)]
                sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
                if sheet:
                    df = pd.read_excel(xls, sheet_name=sheet, header=2)
                    df.columns = df.columns.str.strip()
                    match = df[df['Znak'] == znak]
                    if not match.empty:
                        st.write(f"**{ime} ({znak})**: {match.iloc[0]['Biljka']} | *{match.iloc[0]['Boja']}*")
        except ValueError:
            st.error("Uneti datum ne postoji (proveri broj dana u mesecu).")
