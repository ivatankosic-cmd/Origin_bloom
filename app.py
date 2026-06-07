import streamlit as st
import pandas as pd
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText

# Podešavanje stranice
st.set_page_config(page_title="Origin Bloom", page_icon="🌸", layout="centered")

# ULTRA-PREMIUM CSS STILIZACIJA (Kompaktno, bez praznih redova da ne puca kod)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');
#MainMenu, footer, header {visibility: hidden;}
.stApp {background-color: #FAF9F6;}
html, body, [class*="css"] {font-family: 'Montserrat', sans-serif; color: #2c2c2c;}
h1, h2, h3, h4, h5, h6 {font-family: 'Playfair Display', serif !important; color: #111111; font-weight: 500;}
label, .st-emotion-cache-1y0t1k8, .st-emotion-cache-1jbcvrx {font-family: 'Montserrat', sans-serif !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 2px; color: #888888 !important; padding-bottom: 5px;}
div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] { border: none !important; border-bottom: 1px solid #e5e5e5 !important; border-radius: 0px !important; background-color: transparent !important;}
div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within, div[data-baseweb="select"]:focus-within { border-bottom: 1px solid #B89768 !important;}
.brand-name { font-size: 12px; color: #B89768; letter-spacing: 4px; text-transform: uppercase; text-align: center; margin-bottom: 5px; font-weight: 500;}
.main-title { text-align: center; font-size: 46px !important; margin-bottom: 0px; letter-spacing: 1px;}
.sub-title { text-align: center; font