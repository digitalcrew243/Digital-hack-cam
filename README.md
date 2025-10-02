# Digital Crew 243 — HackCam

![Visuel du projet](https://files.catbox.moe/2vu6pj.jpg)

## Présentation
**Digital Crew 243 — HackCam** est un prototype d’outil serveur léger conçu pour recevoir, décoder et stocker des images envoyées par des clients. L’application expose un endpoint HTTP (`/upload`) qui accepte des payloads JSON contenant une image encodée en Base64 et un identifiant de capture. Les fichiers sont persistés localement dans un répertoire configurable pour post-traitement, analyse ou ingestion.

> Ce projet est prévu pour un usage en laboratoire et pour des tests de sécurité autorisés. Toute utilisation sur des systèmes tiers sans autorisation explicite est interdite et peut être illégale.

---

## Fonctionnalités clés
- Endpoint HTTP `POST /upload` (JSON) pour réception d’images Base64.  
- Stockage normalisé des captures sous la forme `capture_<n>.jpg` dans un répertoire configurable (`/sdcard/digitalcrew243_HackCam` par défaut).  
- Support pour exposer l’instance locale via des tunnels (Cloudflared / Ngrok).  
- Détection automatique de l’architecture pour le binaire ngrok (ARM/x86_64/386).  
- Timeouts et nettoyage de processus pour éviter les processus zombies.

---

## Exigences
- Python 3.8+  
- Flask  
- `curl` (optionnel)  
- `cloudflared` (si vous souhaitez utiliser le tunnel Cloudflare)  
- (Optionnel) `ngrok` si vous préférez ngrok

---

## Installation (Termux / Linux — rapide)
```bash
# Mettre à jour le système
pkg update && pkg upgrade -y

# Installer dépendances système
pkg install python -y
pkg install curl -y
pkg install cloudflared -y

# Installer dépendances Python du projet
pip install -r requirements.txt