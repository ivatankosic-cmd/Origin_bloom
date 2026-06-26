import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import ArcGIS
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
import time

st.set_page_config(page_title="Origin Bloom", page_icon="🌸", layout="centered")

css_kod = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');
#MainMenu, footer, header {visibility: hidden;}
.stApp {background-color: #FAF9F6;}
html, body {font-family: 'Montserrat', sans-serif; color: #2c2c2c;}
h1, h2, h3 {font-family: 'Playfair Display', serif !important; color: #111111;}
.brand-name { font-size: 12px; color: #B89768; letter-spacing: 4px; text-transform: uppercase; text-align: center; margin-bottom: 5px;}
.main-title { text-align: center; font-size: 46px !important; margin-bottom: 0px;}
.sub-title { text-align: center; font-size: 16px; font-style: italic; color: #777; margin-bottom: 15px;}
.gold-divider { width: 40px; height: 1px; background-color: #B89768; margin: 0px auto 40px auto;}
.result-section { background-color: #ffffff; padding: 40px; border: 1px solid #f2f2f2; margin-top: 40px;}
.planet-row { padding: 10px 0; border-bottom: 1px solid #f9f9f9; display: flex; justify-content: space-between;}
.stButton > button { width: 100%; border: 1px solid #2c3e2e !important; padding: 15px; color: #2c3e2e; text-transform: uppercase; letter-spacing: 2px;}
</style>
"""
st.markdown(css_kod, unsafe_allow_html=True)

st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Origin Bloom</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>buket koji te opisuje</p>", unsafe_allow_html=True)
st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

if 'prikazano' not in st.session_state:
    st.session_state.prikazano = False

if 'uspesno_naruceno' not in st.session_state:
    st.session_state.uspesno_naruceno = False

def prikazi_rezultate():
    st.session_state.prikazano = True

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

try:
    xls = pd.ExcelFile('astrologija_biljke.xlsx')
except Exception:
    st.error("Excel fajl nije pronađen.")
    st.stop()

col_lok1, col_lok2 = st.columns(2)
drzava = col_lok1.text_input("Država rođenja")
grad = col_lok2.text_input("Grad rođenja")

col_dan, col_mesec, col_godina = st.columns(3)
dan = col_dan.number_input("Dan", 1, 31, 1)
mesec = col_mesec.number_input("Mesec", 1, 12, 1)
godina = col_godina.number_input("Godina", 1900, 2026, 1990)

col_sat, col_min = st.columns(2)
sati = col_sat.number_input("Sati", 0, 23, 12)
minuti = col_min.number_input("Minuti", 0, 59, 0)

st.button("Prikaži moj buket", on_click=prikazi_rezultate)

if st.session_state.prikazano:
    geolocator = ArcGIS()
    location = geolocator.geocode(f"{grad}, {drzava}", timeout=10)
    
    if not location:
        st.warning("Lokacija nije prepoznata. Probaj veći grad.")
    else:
        tz_str = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude) or "UTC"
        local_tz = pytz.timezone(tz_str)
        lokalno_vreme = datetime(int(godina), int(mesec), int(dan), int(sati), int(minuti))
        
        try:
            lokalno_vreme_sa_zonom = local_tz.localize(lokalno_vreme, is_dst=None)
        except Exception:
            lokalno_vreme_sa_zonom = local_tz.localize(lokalno_vreme, is_dst=False)
            
        utc_vreme = lokalno_vreme_sa_zonom.astimezone(pytz.utc)
        jd = swe.julday(utc_vreme.year, utc_vreme.month, utc_vreme.day, utc_vreme.hour + utc_vreme.minute/60.0)
        znak_ime = ZNACI[int(swe.calc_ut(jd, 0)[0][0] // 30)]
        podznak_ime = ZNACI[int(swe.houses(jd, location.latitude, location.longitude, b'P')[1][0] // 30)]
        
        st.markdown(f"### Znak: {znak_ime} | Podznak: {podznak_ime}")
        
        for id, ime in {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars'}.items():
            znak = ZNACI[int(swe.calc_ut(jd, id)[0][0] // 30)]
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                df.columns = df.columns.str.strip()
                match = df[df['Znak'].str.strip() == znak]
                if not match.empty:
                    st.write(f"{ime} ({znak}): {match.iloc[0]['Biljka']} | {match.iloc[0]['Boja']}")

        if st.session_state.uspesno_naruceno:
            st.success("Hvala! Uskoro te kontaktiramo.")
        else:
            with st.form("forma"):
                ime = st.text_input("Ime i prezime")
                email = st.text_input("Email")
                if st.form_submit_button("Naruči"):
                    st.session_state.uspesno_naruceno = True
                    st.rerun()