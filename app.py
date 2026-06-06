import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import date

# CSS za zelene ivice
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
        
        # SVE planete sa njihovim ID-evima
        sve_planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 
                       5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}
        
        # Logika: Sunce i Mesec su uvek tu (ID 0 i 1)
        # Za ostale, računamo brzinu (planete koje se brže kreću su često ličnije i uticajnije)
        # ili jednostavno uzimamo one koje su u "jakim" znacima (sedište/egzaltacija)
        
        rezultati = []
        for id, ime in sve_planete.items():
            pos = swe.calc_ut(jd, id)[0][0]
            znak_id = int(pos // 30)
            
            # Jednostavan sistem bodovanja snage (sedište = 2, egzaltacija = 1, ostalo = 0)
            snaga = 0
            if znak_id in [0, 4, 1, 5, 2, 6, 3, 7, 8, 11, 9, 10]: # Ovde bi išla prava tabela dostojanstva
                snaga = 1 
            
            rezultati.append({'id': id, 'ime': ime, 'snaga': snaga, 'znak': ZNACI[znak_id]})
        
        # Sortiramo po snazi (Sunce i Mesec ostaju na vrhu)
        rezultati.sort(key=lambda x: (x['id'] > 1, -x['snaga']))
        
        # Uzimamo 5 najdominantnijih
        top_5 = rezultati[:5]
        
        st.success(f"### Tvoj lični cvetni potpis")
        
        for item in top_5:
            ime = item['ime']
            znak_ime = item['znak']
            
            sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
            if sheet:
                df = pd.read_excel(xls, sheet_name=sheet, header=2)
                df.columns = df.columns.str.strip()
                match = df[df['Znak'] == znak_ime]
                if not match.empty:
                    st.write(f"**{ime} ({znak_ime})**: {match.iloc[0]['Biljka']} | *{match.iloc[0]['Boja']}*")