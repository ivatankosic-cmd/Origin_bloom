st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Montserrat:wght@300;400;500&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Topla pozadina nalik premium papiru */
    .stApp {
        background-color: #fbfaf6; 
    }

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        color: #333333;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #1a1a1a;
        font-weight: 600;
    }

    div[data-baseweb="input"] { 
        border: none !important;
        border-bottom: 1px solid #dcdcdc !important; 
        border-radius: 0px !important;
        background-color: transparent !important;
    }
    div[data-baseweb="input"]:focus-within { 
        border-bottom: 1px solid #B89768 !important; /* Zlatna linija kad se klikne na polje */
    }
    
    /* ZLATNI BRAND NAME */
    .brand-name { 
        font-size: 14px; 
        color: #B89768; /* Elegantna stara zlatna boja */
        letter-spacing: 3px; 
        text-transform: uppercase; 
        text-align: center;
        margin-bottom: -10px;
        font-weight: 500;
    }
    .main-title {
        text-align: center;
        font-size: 42px !important;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        font-style: italic;
        color: #666;
        margin-bottom: 40px;
    }

    .result-section {
        background-color: #ffffff; /* Beli okvir na toploj pozadini daje dubinu */
        padding: 40px 30px;
        border-radius: 2px;
        border: 1px solid #eaeaea;
        margin-top: 30px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.03); /* Suptilna senka */
    }
    
    .result-title { font-size: 24px; text-align: center; margin-bottom: 5px; }
    .result-subtitle { font-size: 15px; text-align: center; color: #555; margin-bottom: 30px; }
    
    .planet-row {
        font-size: 16px;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .sun-message { 
        font-family: 'Playfair Display', serif;
        font-size: 18px; 
        font-style: italic; 
        text-align: center; 
        color: #B89768; /* I ličnu poruku možemo u zlatno za lep akcenat */
        margin-top: 35px; 
        margin-bottom: 15px;
    }
    
    .note-text {
        font-size: 13px;
        color: #777;
        text-align: center;
        line-height: 1.6;
        margin-top: 20px;
        padding: 0 20px;
    }

    .art-process {
        margin-top: 50px;
        padding: 0 20px;
    }
    .process-title {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        border-bottom: 1px solid #B89768; /* Zlatna linija ispod naslova */
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .process-text {
        font-size: 15px;
        line-height: 1.8;
        color: #444;
        text-align: justify;
    }

    .stButton>button {
        width: 100%;
        background-color: #2c3e2e !important;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
        letter-spacing: 1px;
        padding: 12px;
        border-radius: 0px;
        border: none;
        margin-top: 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #425c45 !important;
    }
    </style>
""", unsafe_allow_html=True)