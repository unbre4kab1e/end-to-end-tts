import streamlit as st
import subprocess
import os
import time

# Configuration des dossiers
MEL_DIR = "mel_files"
WAV_DIR = "wav_files"
os.makedirs(MEL_DIR, exist_ok=True)
os.makedirs(WAV_DIR, exist_ok=True)

st.title("TTS Pipeline Complet")
st.markdown("**Workflow:** Texte → Tacotron2 → HiFi-GAN → Audio")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("Configuration")
    tacotron_ckpt = st.text_input("Chemin Tacotron2 checkpoint", "./Tacotron2-PyTorch/ckpt_200000.pt")
    hifigan_ckpt = st.text_input("Chemin HiFi-GAN checkpoint", "./hifi-gan/generator_v1")
    text_input = st.text_area("Texte à synthétiser", "Hello World")

# Génération
if st.button("Lancer la synthèse complète"):
    try:
        # Étape 1: Tacotron2
        st.subheader("Étape 1: Génération du Mel-Spectrogramme")
        mel_id = str(int(time.time()))  # ID unique basé sur le timestamp
        mel_path = os.path.join(MEL_DIR, mel_id)
        
        tacotron_cmd = f"python ./Tacotron2-PyTorch/inference.py --ckpt_pth={tacotron_ckpt} --text=\"{text_input}\" --npy_pth={mel_path}"
        process = subprocess.run(tacotron_cmd, shell=True, capture_output=True, text=True)
        
        st.code(f"Commande exécutée:\n{tacotron_cmd}")
        if process.returncode != 0:
            st.error(f"Erreur Tacotron2:\n{process.stderr}")
            raise Exception("Échec de Tacotron2")
        
        st.success(f"Mel généré: {mel_path}.npy")

        # Étape 2: HiFi-GAN
        st.subheader("Étape 2: Synthèse Audio")
        hifigan_cmd = f"python ./hifi-gan/inference_e2e.py --checkpoint_file={hifigan_ckpt} --input_mels_dir={MEL_DIR} --output_dir={WAV_DIR}"
        process = subprocess.run(hifigan_cmd, shell=True, capture_output=True, text=True)
        
        st.code(f"Commande exécutée:\n{hifigan_cmd}")
        if process.returncode != 0:
            st.error(f"Erreur HiFi-GAN:\n{process.stderr}")
            raise Exception("Échec de HiFi-GAN")
        
        # Récupération du fichier généré
        output_wav = os.path.join(WAV_DIR, f"{mel_id}_generated_e2e.wav")
        if not os.path.exists(output_wav):
            raise FileNotFoundError(f"Fichier audio non trouvé: {output_wav}")
        
        st.success("Synthèse audio réussie !")
        st.audio(output_wav)
        
        # Téléchargement
        with open(output_wav, "rb") as f:
            st.download_button(
                "Télécharger l'audio",
                f.read(),
                file_name="synthèse.wav",
                mime="audio/wav"
            )

    except Exception as e:
        st.error(f"Erreur globale: {str(e)}")
        st.markdown("""
            **Erreur:**
            Vérifiez les chemins des checkpoints !!
        """)