import streamlit as st
import pandas as pd
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

# Prevodilac za nazive znakova (mora se podudarati sa tvojom tabelom)
PREVOD = {
    'Aries': 'Ovan', 'Taurus': 'Bik', 'Gemini': 'Blizanci', 'Cancer': 'Rak',
    'Leo': 'Lav', 'Virgo': 'Devica', 'Libra': 'Vaga', 'Scorpio': 'Škorpija',
    'Sagittarius': 'Strelac', 'Capricorn': 'Jarac', 'Aquarius': 'Vodolija', 'Pisces': 'Ribe'
}

st.set_page_config(page_title="Origin Bloom", page_icon="🌸")
st.title("🌸 Origin Bloom - Natalni Recept")

# Učitavanje baze
@st.cache_data
def load_data():
    # Učitava Excel fajl
    return pd.ExcelFile('astrologija_biljke.xlsx')

try:
    xls = load_data()
except:
    st.error("Nisam pronašao 'astrologija_biljke.xlsx'. Proveri naziv fajla!")
    st.stop()

with st.form("input_form"):
    datum = st.date_input("Datum rođenja")
    vreme = st.time_input("Vreme rođenja")
    lat = st.number_input("Geografska širina (npr. 44.81)", format="%.2f")
    lon = st.number_input("Geografska dužina (npr. 20.46)", format="%.2f")
    submitted = st.form_submit_button("Generiši natalni recept")

if submitted:
    # 1. Proračun pozicija
    dt = Datetime(datum.strftime("%Y/%m/%d"), vreme.strftime("%H:%M"), "+00:00")
    chart = Chart(dt, GeoPos(lat, lon))
    
    planete_za_obradu = {
        const.SUN: 'Sunce', const.MOON: 'Mesec', const.MERCURY: 'Merkur', 
        const.VENUS: 'Venera', const.MARS: 'Mars', const.JUPITER: 'Jupiter', 
        const.SATURN: 'Saturn', const.URANUS: 'Uran', const.NEPTUNE: 'Neptun', const.PLUTO: 'Pluton'
    }
    
    st.success("### Tvoj Origin Bloom Recept:")
    
    for p_const, ime_planete in planete_za_obradu.items():
        znak = PREVOD.get(chart.get(p_const).sign)
        
        # Traženje odgovarajućeg taba u Excelu
        sheet_name = next((s for s in xls.sheet_names if ime_planete.lower() in s.lower()), None)
        
        if sheet_name:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=2) # header=2 jer podaci počinju od 3. reda
            match = df[df['Znak'] == znak] 
            
            if not match.empty:
                cvet = match.iloc[0]['Biljka']
                boja = match.iloc[0]['Boja']
                poruka = match.iloc[0]['Poruka']
                st.write(f"**{ime_planete} ({znak})**: {cvet} | *{boja}*")
                st.caption(f"Poruka: {poruka}")