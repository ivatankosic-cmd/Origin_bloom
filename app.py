# ... (sve ostalo ostaje isto, samo zameni blok sa formom ovim dole)

            # SEKCIJA ZA NARUČIVANJE (Premium tekst + Forma)
            st.markdown("""
            <div class='cta-container' style='background-color: transparent; border: none; padding-top: 0;'>
                <b>Origin Bloom</b> je premium, personalizovana slika, ručno crtana na osnovu tvoje natalne karte.<br>
                Svaki potez je unikat, kreiran sa posvećenošću i pažnjom prema detaljima.
            </div>
            """, unsafe_allow_html=True)

            with st.form("forma_za_narucivanje", clear_on_submit=False):
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
                
                # STILIZOVANO CRNO DUGME SA ZLATNIM DETALJIMA
                submit_narudzbina = st.form_submit_button("Pošalji zahtev za izradu")
                
                if submit_narudzbina:
                    if ime_prezime.strip() and email.strip() and telefon.strip() and adresa.strip() and saglasnost_vizija and saglasnost_vreme:
                        st.success("Hvala, tvoj zahtev je uspešno zabeležen! Uskoro ću te kontaktirati.")
                        # OVDE MOŽEMO DODATI KOD ZA AUTOMATSKO SLANJE MAIL-A
                    else:
                        st.error("Molimo vas da popunite sva tekstualna polja i prihvatite oba uslova izrade.")