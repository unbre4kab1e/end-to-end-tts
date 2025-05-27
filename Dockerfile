FROM python:3.9-slim

WORKDIR /app
COPY . /app

# 1) Mettre à jour pip
RUN pip install --upgrade pip

# 2) Installer explicitement Streamlit avant le reste
RUN pip install streamlit

# 3) Installer PyTorch CPU et les autres dépendances
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r requirements.txt

# 4) Exposer le port Streamlit
EXPOSE 8501

# 5) Lancer Streamlit via python -m pour éviter les soucis de PATH
ENTRYPOINT ["python","-m","streamlit","run","app.py",\
  "--server.address=0.0.0.0",\
  "--server.port=8501",\
  "--server.enableXsrfProtection=false",\
  "--server.enableCORS=false"]