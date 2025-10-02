#!/usr/bin/env bash
cat > README.md <<'EOF'
# Digital Crew 243 — HackCam

![Visuel du projet](https://files.catbox.moe/2vu6pj.jpg)

**Définition**  
Digital Crew 243 — HackCam est un prototype serveur léger conçu pour recevoir, décoder et stocker des images envoyées par des clients via un endpoint HTTP.

**Fonctions principales**  
- Endpoint `/upload` acceptant un JSON contenant une image (base64) et un identifiant.  
- Persistance locale des captures dans `/sdcard/digitalcrew243_HackCam`.  
- Détection d'architecture et gestion des binaires de tunnel (ngrok/cloudflared).  
- Récupération et affichage de l'URL publique fournie par le tunnel.

**Architecture & flux**  
1. Client encode l'image en base64 et POSTe au serveur.  
2. Serveur décode et sauvegarde `capture_<n>.jpg`.  
3. Opérateur lance un tunnel pour exposer `http://localhost:5000` si nécessaire.  
4. Captures disponibles localement pour traitement.

**Aspects techniques**  
- Séparation claire entre API (Flask) et gestion des tunnels.  
- Support multi-architecture pour le téléchargement des binaires.  
- Timeouts et nettoyage des processus pour robustesse opérationnelle.

**Cas d'usage**  
- Simulations en laboratoire et validation de pipelines de collecte d'images.  
- Tests contrôlés pour procédures de détection et forensics.

Digital Crew 243 — HackCam
EOF
echo "README.md créé."