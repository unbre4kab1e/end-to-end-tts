# End-To-End TTS Complet

Ce dépôt contient :

* **Notebook pour reproduire notre système :** `lab_final.ipynb`
* **Application Streamlit :** `app.py`

---

## Exécution

1. **Notebook** :

   ```bash
   jupyter lab lab_final.ipynb
   ```

2. **Application** :

   ```bash
   streamlit run app.py
   ```

C'est tout !

---

## Entraînement du modèle Tacotron2 & HiFi-GAN

Si vous souhaitez **entraîner les modèles** sur vos propres données ou reproduire notre processus complet :

1. **Préparation des données** :

   * Placez vos fichiers WAV dans `data/wav_files/`.
   * Générez les spectrogrammes Mel avec :

     ```bash
     python prepare_data.py --input_dir data/wav_files --output_dir data/mel_files
     ```

2. **Entraînement Tacotron2** :

   ```bash
   python train_tacotron2.py \
     --data_dir data/mel_files \
     --output_dir checkpoints/tacotron2 \
     --epochs 1000 \
     --batch_size 32
   ```

   > **Note** : l’entraînement sur le dataset LJSpeech prend **plusieurs jours** sur un GPU unique pour converger.

> **Statut** : nous avons interrompu le processus d’entraînement en raison du temps nécessaire pour compléter la formation.

3. **Entraînement HiFi-GAN** :

   ```bash
   python train_hifigan.py \
     --config hifigan/config.json \
     --data_dir data/mel_files \
     --output_dir checkpoints/hifigan \
     --epochs 500
   ```

   > **Astuce** : utilisez plusieurs GPUs ou un cluster pour réduire le temps d’entraînement.

4. **Évaluation et export** :

   * Générer un échantillon audio pour valider la qualité :

     ```bash
     python inference.py \
       --tacotron_ckpt checkpoints/tacotron2/model.pt \
       --hifigan_ckpt checkpoints/hifigan/generator.pt \
       --text "Votre texte de test"
     ```

---

Abdelghafour MOUJAHIDDINE
EL Amine Biyad
MIT
