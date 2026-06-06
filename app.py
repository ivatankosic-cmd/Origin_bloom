import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import date

st.title("🌸 Origin Bloom - Natalni Recept")

# Učitavanje
def load_excel():
    return pd.ExcelFile('astrologija_biljke.xlsx')

try:
    xls = load_excel()
except Exception as e:
    st.error(f"Nisam našao Excel fajl: {e}")
    st.stop()

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

# Forma
grad = st.text_input("Grad i Država (npr. Beograd, Srbija)")
datum = st.date_input("Datum rođenja", min_value=date(1900, 1, 1))

col1, col2 = st.columns(2)
sati = col1.number_input("Sati", min_value=0, max_value=23, value=12)
minuti = col2.number_input("Minuti", min_value=0, max_value=59, value=0)

if st.button("Generiši recept"):
    geolocator = Nominatim(user_agent="origin_bloom_app")
    location = geolocator.geocode(grad)
    
    if not location:
        st.error("Nisam pronašao grad.")
    else:
        jd = swe.julday(datum.year, datum.month, datum.day, sati + minuti/60)
        planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 
                   5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}
        
        st.success(f"### Recept za: {grad}")
        
        for id, ime in planete.items():
            pos = swe.calc_ut(jd, id)[0][0]
            znak_id = int(pos // 30)
            znak_ime = ZNACI[znak_id]
            
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                # header=2 preskače prva dva reda, a .str.strip() čisti nazive kolona
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                df.columns = df.columns.str.strip() 
                
                match = df[df['Znak'] == znak_ime]
                if not match.empty:
                    cvet = match.iloc[0]['Biljka']
                    boja = match.iloc[0]['Boja']
                    poruka = match.iloc[0]['Poruka']
                    st.write(f"**{ime} ({znak_ime})**: {cvet} | *{boja}*")
                    st.caption(f"Poruka: {poruka}")