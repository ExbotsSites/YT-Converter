import streamlit as st
import yt_dlp
import os
from captcha.image import ImageCaptcha
import random
import string
from io import BytesIO

st.title("YouTube Downloader Online con CAPTCHA")

# --- Funzione per generare CAPTCHA ---
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    image = ImageCaptcha()
    image_data = image.generate(captcha_text)
    image_bytes = BytesIO(image_data.read())
    return captcha_text, image_bytes

# --- Inizializza CAPTCHA ---
if "captcha_text" not in st.session_state or "captcha_image" not in st.session_state:
    st.session_state.captcha_text, st.session_state.captcha_image = generate_captcha()

st.image(st.session_state.captcha_image)

# --- Input utente memorizzato ---
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_input("Inserisci il testo del CAPTCHA:", value=st.session_state.user_input)

# --- Link YouTube e formato ---
url = st.text_input("Inserisci il link del video YouTube:")
format_choice = st.radio("Formato:", ("Video", "Audio"))

# --- Pulsante Scarica ---
if st.button("Scarica"):
    if not url:
        st.warning("Inserisci un link valido!")
    elif st.session_state.user_input.upper() != st.session_state.captcha_text:
        st.error("CAPTCHA errato. Riprova.")
        # Rigenera CAPTCHA se sbagliato
        st.session_state.captcha_text, st.session_state.captcha_image = generate_captcha()
        st.session_state.user_input = ""  # reset input
    else:
        try:
            st.info("Inizio download...")

            ydl_opts = {
                'format': 'best' if format_choice == "Video" else 'bestaudio',
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, "rb") as f:
                st.download_button(
                    label="Scarica sul tuo PC",
                    data=f,
                    file_name=os.path.basename(filename),
                    mime="video/mp4" if format_choice=="Video" else "audio/mpeg"
                )

            st.success("Download completato! Clicca il pulsante per salvare il file sul PC.")
            # Rigenera CAPTCHA dopo download
            st.session_state.captcha_text, st.session_state.captcha_image = generate_captcha()
            st.session_state.user_input = ""  # reset input

        except Exception as e:
            st.error(f"Errore durante il download: {e}")