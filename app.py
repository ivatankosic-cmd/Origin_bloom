import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import date

# Stil za zelene okvire
st.markdown("""
    <style>
    div[data-baseweb="input"] { border: 2px solid #A8C69F !important; }
    div[data-baseweb="input"]:focus-within { border: 2px solid #4CAF50 !important; }
    h1 { font-size: 28px !important; }
    .brand-name { font-size: 16px; color: #777; letter-spacing: 2px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# Branding
st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.title("🌸Origin Bloom")
st.subheader("buket koji te opisuje")

def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

try:
    xls = load_excel()
except Exception as e:
    st.error(f"Excel fajl nije učitan: {e}")
    st.stop()

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

# Unos
drzava = st.text_input("Država rođenja")
grad = st.text_input("Grad rođenja")
datum = st.date_input("Datum rođenja", min_value=date(1900, 1, 1))
col1, col2 = st.columns(2)
sati = col1.number_input("Sati", 0, 23, 12)
minuti = col2.number_input("Minuti", 0, 59, 0)

if st.button("prikaži moje cveće"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    lokacija_string = f"{grad}, {drzava}"
    location = geolocator.geocode(lokacija_string)
    
    if not location:
        st.error("Nisam pronašao grad i državu. Proveri unos.")
    else:
        jd = swe.julday(datum.year, datum.month, datum.day, sati + minuti/60)
        
        # Računanje znaka i podznaka
        pos_sunce = swe.calc_ut(jd, 0)[0][0]
        znak_ime = ZNACI[int(pos_sunce // 30)]
        
        cusps, ascmc = swe.houses(jd, location.latitude, location.longitude, b'P')
        podznak_ime = ZNACI[int(ascmc[0] // 30)]
        
        st.success("### Tvoj lični pečat")
        st.write(f"**Znak:** {znak_ime} | **Podznak:** {podznak_ime}")
        st.divider()
        
        # Sortiranje i izbor 5 planeta
        rezultati = []
        for id, ime in {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 
                        5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}.items():
            pos = swe.calc_ut(jd, id)[0][0]
            rezultati.append({'id': id, 'ime': ime, 'znak': ZNACI[int(pos // 30)]})
        
        # Uzimamo 5 najvažnijih (Sunce, Mesec + prve 3 po ID-u)
        top_5 = rezultati[:5]
        
        for item in top_5:
            ime, znak = item['ime'], item['znak']
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                df.columns = df.columns.str.strip()
                match = df[df['Znak'] == znak]
                if not match.empty:
                    st.write(f"**{ime} ({znak})**: {match.iloc[0]['Biljka']} | *{match.iloc[0]['Boja']}*")