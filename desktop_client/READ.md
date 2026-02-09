# 🖥️ Desktop Client (Tkinter)

Namizna aplikacija za upravljanje igralcev in igranje mini "Card Battle" igre.  
Povezana je z backend strežnikom preko REST API.

## 🚀 Zagon

cd desktop_client
python client.py

Backend mora biti zagnan na http://127.0.0.1:5001.

## 🔧 Funkcije

Prikaz vseh igralcev (GET /players)
Dodajanje igralca
Urejanje rezultata
Brisanje igralca
Dnevna nagrada
Izbira 2 herojev (Warrior, Mage, Rogue, Paladin, Hunter)
Enostavna "Card Battle" mini igra (Attack / Defend / Special)

## 🖼️ UI

Temna neon tema
Seznam igralcev (TreeView)
Ločeno okno za izbor herojev
Ločeno okno za bitko z HP indikatorji

## 📡 Backend povezava

Aplikacija uporablja API:

http://127.0.0.1:5001

Podatki med web klientom in desktop klientom so isti → delijo isto bazo.

## 📁 Struktura
desktop_client/
│── client.py
└── README.md

## ⚠️ Opombe

Bitka deluje samo, če sta izbrana 2 heroja.

Če battle stanje izgine, backend je bil restartan → začni novo bitko.