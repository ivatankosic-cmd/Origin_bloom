import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import date

# CSS za promenu boje uokvirivanja sa crvene na nežno zelenu
st.markdown("""
    <style>
    .stTextInput > div > div > input:focus {
        border-color: #A8C69F !important;
        box-shadow: 0 0 0 0.1rem #A8C69F !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌸 Origin Bloom 🌸")
st.subheader("buket koji te opisuje")

def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

try:
    xls = load_excel()
except Exception as e:
    st.error(f"Excel fajl nije pronađen: {e}")
    st.stop()

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

grad = st.text_input("Grad i Država")
datum = st.date_input("Datum rođenja", min_value=date(1900, 1, 1))

col1, col2 = st.columns(2)
sati = col1.number_input("Sati", min_value=0, max_value=23, value=12)
minuti = col2.number_input("Minuti", min_value=0, max_value=59, value=0)

if st.button("prikaži moje cveće"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    location = geolocator.geocode(grad)
    
    if not location:
        st.error("Nisam pronašao taj grad. Proveri unos.")
    else:
        jd = swe.julday(datum.year, datum.month, datum.day, sati + minuti/60)
        planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 
                   5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}
        
        st.success(f"### Tvoj lični cvetni potpis")
        
        for id, ime in planete.items():
            pos = swe.calc_ut(jd, id)[0][0]
            znak_id = int(pos // 30)
            znak_ime = ZNACI[znak_id]
            
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                df.columns = df.columns.str.strip()
                match = df[df['Znak'] == znak_ime]
                if not match.empty:
                    st.write(f"**{ime} ({znak_ime})**: {match.iloc[0]['Biljka']} | *{match.iloc[0]['Boja']}*")