import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import date

# 1. Definisanje funkcije BEZ KEŠIRANJA (obriši @st.cache_data)
def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

# 2. Učitavanje fajla
xls = load_excel()

# Prevodilac znakova (0-11)
ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

st.title("🌸 Origin Bloom - Natalni Recept")

# Forma
grad = st.text_input("Grad i Država (npr. Beograd, Srbija)")
datum = st.date_input("Datum rođenja", min_value=date(1900, 1, 1))
vreme = st.time_input("Vreme rođenja")

if st.button("Generiši recept"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    location = geolocator.geocode(grad)
    
    if not location:
        st.error("Nisam pronašao grad.")
    else:
        jd = swe.julday(datum.year, datum.month, datum.day, vreme.hour + vreme.minute/60)
        planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 
                   5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}
        
        for id, ime in planete.items():
            pos = swe.calc_ut(jd, id)[0][0]
            znak_id = int(pos // 30)
            znak_ime = ZNACI[znak_id]
            
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                match = df[df['Znak'] == znak_ime]
                if not match.empty:
                    st.write(f"**{ime} ({znak_ime})**: {match.iloc[0]['Biljka']} | *{match.iloc[0]['Boja']}*")