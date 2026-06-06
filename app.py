import streamlit as st
import pandas as pd
import swisseph as swe

# Prevodilac znakova (flatlib vraća engleske nazive, mi ćemo koristiti brojeve znaka 0-11)
ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

st.title("🌸 Origin Bloom")

# Učitavanje baze


xls = load_data()

datum = st.date_input("Datum rođenja")
vreme = st.time_input("Vreme rođenja")
# Za sada ručno, možemo posle automatizovati
lat = st.number_input("Geografska širina", 44.81)
lon = st.number_input("Geografska dužina", 20.46)

if st.button("Generiši recept"):
    # Računanje pozicije planeta
    jd = swe.julday(datum.year, datum.month, datum.day, vreme.hour + vreme.minute/60)
    
    planete = {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars', 5: 'Jupiter', 6: 'Saturn', 7: 'Uran', 8: 'Neptun', 9: 'Pluton'}
    
    for id, ime in planete.items():
        pos = swe.calc_ut(jd, id)[0][0]
        znak_id = int(pos // 30)
        znak_ime = ZNACI[znak_id]
        
        # Pronalaženje u Excelu
        sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
        if sheet:
            df = pd.read_excel(xls, sheet_name=sheet, header=2)
            match = df[df['Znak'] == znak_ime]
            if not match.empty:
                st.write(f"**{ime} ({znak_ime})**: {match.iloc[0]['Biljka']} | {match.iloc[0]['Boja']}")
