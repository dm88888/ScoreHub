@"
# Installation Guide

## 1. Backend Setup
Open PowerShell:

cd backend
pip install -r requirements.txt
python app.py

Backend runs at:
http://127.0.0.1:5001

## 2. Desktop Client
cd desktop_client
python client.py

## 3. Web Client
Open:
web_client/index.html
in any browser (Chrome recommended).
"@ | Set-Content docs/installation_guide.md
