import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
import time  # Dodato za pauziranje

st.set_page_config(page_title="Origin Bloom", page_icon="🌸", layout="centered")

css_kod = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');
#MainMenu, footer, header {visibility: hidden;}
.stApp {background-color: #FAF9F6;}
html, body, [class*="css"] {font-family: 'Montserrat', sans-serif; color: #2c2c2c;}
h1, h2, h3, h4, h5, h6 {font-family: 'Playfair Display', serif !important; color: #111111; font-weight: 500;}
label {font-family: 'Montserrat', sans-serif !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 2px; color: #888888 !important; padding-bottom: 5px;}
div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] { border: none !important; border-bottom: 1px solid #e5e5e5 !important; border-radius: 0px !important; background-color: transparent !important;}
div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within, div[data-baseweb="select"]:focus-within { border-bottom: 1px solid #B89768 !important;}
.brand-name { font-size: 12px; color: #B89768; letter-spacing: 4px; text-transform: uppercase; text-align: center; margin-bottom: 5px; font-weight: 500;}
.main-title { text-align: center; font-size: 46px !important; margin-bottom: 0px; letter-spacing: 1px;}
.sub-title { text-align: center; font-size: 16px; font-family: 'Playfair Display', serif; font-style: italic; color: #777; margin-bottom: 15px;}
.gold-divider { width: 40px; height: 1px; background-color: #B89768; margin: 0px auto 40px auto;}
.result-section { background-color: #ffffff; padding: 50px 40px; border: 1px solid #f2f2f2; margin-top: 40px; box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.02);}
.result-title { font-size: 26px; text-align: center; margin-bottom: 10px;}
.result-subtitle { font-size: 14px; text-align: center; color: #666; margin-bottom: 40px; line-height: 1.6;}
.astrology-header { text-align: center; margin-bottom: 30px; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #888;}
.planet-row { font-size: 15px; padding: 12px 0; border-bottom: 1px solid #f9f9f9; display: flex; justify-content: space-between; align-items: center;}
.planet-name { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #999; font-weight: 500;}
.planet-result { font-family: 'Playfair Display', serif; font-style: italic; font-size: 17px; color: #222; text-align: right;}
.sun-message { font-family: 'Playfair Display', serif; font-size: 19px; font-style: italic; text-align: center; color: #B89768; margin-top: 45px; margin-bottom: 25px; line-height: 1.5;}
.note-text { font-size: 11px; color: #a0a0a0; text-align: center; line-height: 1.8; margin-top: 35px; padding: 0 10px; text-transform: uppercase; letter-spacing: 1px;}
.art-process { margin-top: 60px; padding: 0 20px; margin-bottom: 40px;}
.process-title { font-family: 'Playfair Display', serif; font-size: 20px; text-align: center; margin-top: 40px; margin-bottom: 15px; color: #222;}
.process-text { font-size: 14px; line-height: 2; color: #555; text-align: center; font-weight: 300;}
.cta-container { text-align: center; padding: 35px 30px; margin-top: 50px; font-size: 14px; color: #444; line-height: 1.8;}
.stButton > button { width: 100%; background-color: transparent !important; color: #2c3e2e !important; font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; padding: 15px; border: 1px solid #2c3e2e !important; margin-top: 30px; transition: all 0.4s ease;}
.stButton > button:hover { background-color: #2c3e2e !important; color: white !important;}
.stFormSubmitButton > button { width: 100%; background-color: #111111 !important; color: #B89768 !important; font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 3px; padding: 18px; border: 1px solid #B89768 !important; margin-top: 20px; transition: all 0.4s ease;}
.stFormSubmitButton > button:hover { background-color: #B89768 !important; color: #111111 !important; border: 1px solid #111111 !important;}
</style>
"""
st.markdown(css_kod, unsafe_allow_html=True)

st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Origin Bloom</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>buket koji te opisuje</p>", unsafe_allow_html=True)
st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

if 'prikazano' not in st.session_state: st.session_state.prikazano = False
if 'uspesno_naruceno' not in st.session_state: st.session_state.uspesno_naruceno = False

def prikazi_rezultate(): st.session_state.prikazano = True

ZNACI = ['Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']

try: xls = pd.ExcelFile('astrologija_biljke.xlsx')
except Exception: st.error("Excel fajl nije pronađen."); st.stop()

col_lok1, col_lok2 = st.columns(2)
drzava = col_lok1.text_input("Država rođenja")
grad = col_lok2.text_input("Grad rođenja")

st.write("") 
st.markdown("<div style='margin-bottom: -15px;'><label>Datum rođenja</label></div>", unsafe_allow_html=True)
col_dan, col_mesec, col_godina = st.columns(3)
dan = col_dan.number_input("Dan", 1, 31, 1)
mesec = col_mesec.number_input("Mesec", 1, 12, 1)
godina = col_godina.number_input("Godina", 1900, 2026, 1990)

st.write("")
st.markdown("<div style='margin-bottom: -15px;'><label>Vreme rođenja</label></div>", unsafe_allow_html=True)
col_sat, col_min = st.columns(2)
sati = col_sat.number_input("Sati", 0, 23, 12)
minuti = col_min.number_input("Minuti", 0, 59, 0)

st.button("Prikaži moj buket", on_click=prikazi_rezultate)

if st.session_state.prikazano:
    # Potpuno unikatan User-Agent kako nas mape ne bi blokirale
    geolocator = Nominatim(user_agent="ethereal_origin_bloom_iva_12345")
    location = None
    
    # Prvi pokušaj traženja lokacije
    try:
        location = geolocator.geocode(f"{grad}, {drzava}", timeout=10)
    except Exception:
        # Ako prvi put pukne, sačekaj 2 sekunde pa probaj ponovo tajno
        time.sleep(2)
        try:
            location = geolocator.geocode(f"{grad}, {drzava}", timeout=10)
        except Exception:
            pass # Pustićemo da prođe u sledeći blok i izbaci grešku
    
    if not location:
        st.warning("Servis za mape trenutno obrađuje previše zahteva ili lokacija nije prepoznata. Molim te proveri unos (probaj da uneseš veći obližnji grad) i klikni dugme ponovo.")
    else:
        try:
            tz_str = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude) or "UTC"
            local_tz = pytz.timezone(tz_str)
            lokalno_vreme = datetime(int(godina), int(mesec), int(dan), int(sati), int(minuti))
            try: lokalno_vreme_sa_zonom = local_tz.localize(lokalno_vreme, is_dst=None)
            except: lokalno_vreme_sa_zonom = local_tz.localize(lokalno_vreme, is_dst=False)
            utc_vreme = lokalno_vreme_sa_zonom.astimezone(pytz.utc)
            jd = swe.julday(utc_vreme.year, utc_vreme.month, utc_vreme.day, utc_vreme.hour + utc_vreme.minute/60.0)
            znak_ime = ZNACI[int(swe.calc_ut(jd, 0)[0][0] // 30)]
            podznak_ime = ZNACI[int(swe.houses(jd, location.latitude, location.longitude, b'P')[1][0] // 30)]
            
            # 1. SEKCIJA: Rezultati
            rez_html = f"<div class='result-section'><h2 class='result-title'>Tvoj Origin Bloom profil je kreiran.</h2><p class='result-subtitle'>Precizni podaci prevedeni su u tvoj jedinstveni botanički i koloritni potpis.</p><div class='astrology-header'>Znak: <b>{znak_ime}</b> &nbsp;|&nbsp; Podznak: <b>{podznak_ime}</b></div>"
            poruka_sunce = "" 
            for id, ime in {0: 'Sunce', 1: 'Mesec', 2: 'Merkur', 3: 'Venera', 4: 'Mars'}.items():
                znak = ZNACI[int(swe.calc_ut(jd, id)[0][0] // 30)]
                sheet = next((s for s in xls.sheet_names if ime.lower() in s.lower()), None)
                if sheet:
                    df = pd.read_excel(xls, sheet_name=sheet, header=2)
                    df.columns = df.columns.str.strip()
                    match = df[df['Znak'].str.strip() == znak]
                    if not match.empty:
                        biljka = match.iloc[0]['Biljka']; boja = match.iloc[0]['Boja']
                        rez_html += f"<div class='planet-row'><span class='planet-name'>{ime} ({znak})</span><span class='planet-result'>{biljka} | <span style='color:#B89768;'>{boja}</span></span></div>"
                        if id == 0 and 'Poruka' in match.columns: poruka_sunce = match.iloc[0]['Poruka']
            if poruka_sunce: rez_html += f"<div class='sun-message'>✨ {poruka_sunce}</div>"
            rez_html += "<p class='note-text'>Ovo je sirovi materijal tvog identiteta.<br>Iako ove boje i oblici na prvi pogled možda deluju nespojivo, njihov pravi estetski potencijal otkriva se tek kroz umetničku sintezu.</p></div>"
            st.markdown(rez_html, unsafe_allow_html=True)
            
            # 2. SEKCIJA: Umetnički proces i očekivanja
            st.markdown("<div class='art-process'><h3 class='process-title'>Od koda do kompozicije</h3><p class='process-text'>Ovde se završava proračun i počinje umetnost. Na osnovu tvog koda, ručno osmišljavam kompoziciju, tražim savršen balans između dodeljenih nijansi i oblika. Kroz igru odnosa figure i pozadine, svaki element dobija svoj prostor, gradeći harmoničnu celinu.</p><h3 class='process-title'>Vreme izrade</h3><p class='process-text'>Proces kreiranja ovakvog dela zahteva vreme, mir i slojevitu izgradnju akvarela uz korišćenje premium papira i specifičnih tehnika. Zbog mog posvećenog pristupa svakom unikatnom delu, rok za izradu tvog personalizovanog Origin Bloom originala je 3 nedelje.</p></div>", unsafe_allow_html=True)
            
            # 2.5 NOVA SEKCIJA: Specifikacija ponude i cena
            st.markdown("<div class='investment-section' style='padding: 0 20px; margin-bottom: 50px;'><h3 class='process-title'>Tvoja investicija u unikatno delo</h3><p class='process-text' style='text-align: center; font-weight: 500; color: #B89768; font-size: 16px; margin-bottom: 25px;'>Cena personalizovanog Origin Bloom originala iznosi 150 EUR (format 30x40 cm).</p><p class='process-text' style='margin-bottom: 15px; text-align: left;'>Ova investicija obuhvata:</p><ul style='font-size: 14px; line-height: 1.8; color: #555; font-weight: 300; padding-left: 20px; text-align: left;'><li style='margin-bottom: 8px;'><b>Detaljnu analizu</b> tvog botaničkog koda i osmišljavanje unikatne kompozicije.</li><li style='margin-bottom: 8px;'><b>Manuelni rad</b> uz korišćenje najkvalitetnijih pigmenata i premium akvarel papira.</li><li style='margin-bottom: 8px;'><b>Sertifikat autentičnosti</b>, kao garanciju originalnosti dela.</li><li style='margin-bottom: 8px;'><b>Beleške autora</b> – kratak, personalizovani zapis u kom ti otkrivam simboliku i estetske razloge iza odabranih elemenata na tvojoj slici.</li><li style='margin-bottom: 8px;'><b>Pažljivo i elegantno pakovanje</b>, spremno za bezbednu dostavu ili darivanje.</li></ul></div>", unsafe_allow_html=True)
            
            # 3. SEKCIJA: Forma za naručivanje i zahvalnica
            if st.session_state.uspesno_naruceno:
                st.markdown("<div style='background-color: #ffffff; border: 1px solid #B89768; padding: 50px 30px; text-align: center; margin-top: 40px; box-shadow: 0px 10px 30px rgba(0,0,0,0.02);'><h2 style='color: #B89768; font-family: \"Playfair Display\", serif; font-size: 28px; margin-bottom: 15px;'>Hvala što ste naručili!</h2><p style='color: #444; font-size: 15px; line-height: 1.8; margin-bottom: 0;'>Vaš zahtev za izradu je uspešno zabeležen.<br>Uskoro ćemo vas kontaktirati kako bismo finalizovali detalje.</p></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='cta-container'><b>Origin Bloom</b> je premium, personalizovana slika, ručno crtana na osnovu tvoje natalne karte.<br>Svaki potez je unikat, kreiran sa posvećenošću i pažnjom prema detaljima.<br><br><b>Broj komada na mesečnom nivou je strogo limitiran, jer se svaki primerak pažljivo i ručno stvara.</b></div>", unsafe_allow_html=True)
                with st.form("forma_za_narucivanje", clear_on_submit=True):
                    st.markdown("<h3 class='process-title' style='margin-top: 10px; border-bottom: none;'>Naruči svoj Origin Bloom original</h3>", unsafe_allow_html=True)
                    col_ime, col_email = st.columns(2)
                    ime_prezime = col_ime.text_input("Ime i prezime")
                    email = col_email.text_input("Email adresa")
                    telefon = st.text_input("Broj telefona (potrebno za kurirsku službu)")
                    adresa = st.text_area("Puna adresa za dostavu")
                    namena = st.selectbox("Namena dela", ["Za moj prostor", "Poklon za godišnjicu", "Poklon za rođenje", "Drugo"])
                    st.markdown("<br>", unsafe_allow_html=True)
                    saglasnost_vizija = st.checkbox("Slažem se sa vizijom umetnice i kompoziciju prepuštam njenom autoritetu.")
                    saglasnost_vreme = st.checkbox("Razumem da proces ručne izrade traje 3 nedelje i da je svako delo unikatno.")
                    
                    if st.form_submit_button("Pošalji zahtev za izradu"):
                        if ime_prezime.strip() and email.strip() and telefon.strip() and adresa.strip() and saglasnost_vizija and saglasnost_vreme:
                            poruka_mail = f"NOVA PORUDŽBINA - Origin Bloom\n\nIme: {ime_prezime}\nEmail: {email}\nTelefon: {telefon}\nAdresa: {adresa}\nNamena: {namena}\nZnak: {znak_ime} | Podznak: {podznak_ime}\nFormat: 30x40 cm | Cena: 150 EUR"
                            msg = MIMEText(poruka_mail)
                            msg['Subject'] = f'Nova porudzbina: {ime_prezime} (Origin Bloom)'
                            try:
                                mail_adresa = st.secrets["EMAIL_USER"]
                                mail_lozinka = st.secrets["EMAIL_PASS"]
                                
                                msg['From'] = mail_adresa
                                msg['To'] = mail_adresa
                                
                                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                server.login(mail_adresa, mail_lozinka)
                                server.send_message(msg)
                                server.quit()
                                
                                st.session_state.uspesno_naruceno = True
                                st.rerun()
                            except Exception as e: 
                                st.error(f"Sistem je prijavio grešku pri slanju: {e}")
                        else: 
                            st.error("Molimo vas da popunite sva tekstualna polja i prihvatite oba uslova izrade.")
        except ValueError: st.error("Uneti datum ne postoji (proveri broj dana u mesecu).")
