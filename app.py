import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import date

# Agresivniji CSS za zelene ivice
st.markdown("""
    <style>
    div[data-baseweb="input"] { border: 2px solid #A8C69F !important; }
    div[data-baseweb="input"]:focus-within { border: 2px solid #4CAF50 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🌸 Origin Bloom 🌸")
st.subheader("buket koji te opisuje")

def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

xls = load_excel()
ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

grad = st.text_input("Grad i Država")
datum = st.date_input("Datum rođenja", min_value=date(1900, 1, 1))
col1, col2 = st.columns(2)
sati = col1.number_input("Sati", 0, 23, 12)
minuti = col2.number_input("Minuti", 0, 59, 0)

if st.button("prikaži moje cveće"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    location = geolocator.geocode(grad)
    if not location:
        st.error("Nisam pronašao grad.")
    else:
        jd = swe.julday(datum.year, datum.month, datum.day, sati + minuti/60)
        
        # SVE planete za kalkulaciju snage
        sve_planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 
                       5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}
        
        # Logika: Sunce i Mesec + 2 najbrže (Merkur i Venera su često najdominantnije)
        # Možeš ovde menjati redosled ako želiš druge planete
        dominantne = [0, 1, 2, 3] 
        
        st.success(f"### Tvoj lični cvetni potpis")
        
        for id in dominantne:
            ime = sve_planete[id]
            pos = swe.calc_ut(jd, id)[0][0]
            znak_ime = ZNACI[int(pos // 30)]
            
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                df.columns = df.columns.str.strip()
                match = df[df['Znak'] == znak_ime]
                if not match.empty:
                    st.write(f"**{ime} ({znak_ime})**: {match.iloc[0]['Biljka']} | *{match.iloc[0]['Boja']}*")