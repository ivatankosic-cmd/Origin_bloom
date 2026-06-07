import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Origin Bloom", page_icon="🌸", layout="centered")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');
#MainMenu, footer, header {visibility: hidden;}
.stApp {background-color: #FAF9F6;}
html, body, [class*="css"] {font-family: 'Montserrat', sans-serif; color: #2c2c2c;}
h1, h2, h3, h4, h5, h6 {font-family: 'Playfair Display', serif !important; color: #111111; font-weight: 500;}
label {font-family: 'Montserrat', sans-serif !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 2px; color: #888888 !important; padding-bottom: 5px;}
div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] { border: none !important; border-bottom: 1px solid #e5e5e5 !important; border-radius: 0px !important; background-color: transparent !important;}
div[data-baseweb="input"]:focus-within { border-bottom: 1px solid #B89768 !important;}
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
.process-title { font-family: 'Playfair Display', serif; font-size: 20px; text-align: center; margin-top: 40px; margin-bottom: 15px; color: #222;}
.process-text { font-size: 14px; line-height: 2; color: #555; text-align: center; font-weight: 300;}
.cta-container { text-align: center; padding: 35px 30px; margin-top: 50px; font-size: 14px; color: #444; line-height: 1.8;}
.stButton > button { width: 100%; background-color: transparent !important; color: #2c3e2e !important; font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; padding: 15px; border: 1px solid #2c3e2e !important; margin-top: 30px;}
.stFormSubmitButton > button { width: 100%; background-color: #111111 !important; color: #B89768 !important; font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 3px; padding: 18px; border: 1px solid #B89768 !important; margin-top: 20px;}
</style>""", unsafe_allow_html=True)

st.markdown("<p class='brand-name'>ethereal by iva</p>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Origin Bloom</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>buket koji te opisuje</p>", unsafe_allow_html=True)
st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

if 'prikazano' not in st.session_state: st.session_state.prikazano = False
if 'uspesno_naruceno' not in st.session_state: st.session_state.uspesno_naruceno = False

def prikazi_rezultate(): st.session_state.prikazano = True

col_lok1, col_lok2 = st.columns(2)
drzava = col_lok1.text_input("Država rođenja")
grad = col_lok2.text_input("Grad rođenja")
col_dan, col_mesec, col_godina = st.columns(3)
dan = col_dan.number_input("Dan", 1, 31, 1)
mesec = col_mesec.number_input("Mesec", 1, 12, 1)
godina = col_godina.number_