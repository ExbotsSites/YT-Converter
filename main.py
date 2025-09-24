import streamlit as st
import yt_dlp
import os

st.title("YouTube Downloader Online (senza FFmpeg)")

# Link già inserito come esempio
url = st.text_input(
    "Inserisci il link del video YouTube:", 
    value="https://youtu.be/pxA7z_IXyXM?si=pNgvF9eVmyC4JIjc"
)

# Scegli formato
format_choice = st.radio("Formato:", ("Video", "Audio"))

if st.button("Scarica"):
    if not url:
        st.warning("Inserisci un link valido!")
    else:
        try:
            st.info("Inizio download...")

            # Scarica senza merge: nessun FFmpeg richiesto
            ydl_opts = {
                'format': 'best' if format_choice == "Video" else 'bestaudio',
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Pulsante per scaricare sul PC
            with open(filename, "rb") as f:
                st.download_button(
                    label="Scarica sul tuo PC",
                    data=f,
                    file_name=os.path.basename(filename),
                    mime="video/mp4" if format_choice=="Video" else "audio/mpeg"
                )

            st.success("Download completato! Clicca il pulsante per salvare il file sul PC.")

        except Exception as e:
            st.error(f"Errore durante il download: {e}")
