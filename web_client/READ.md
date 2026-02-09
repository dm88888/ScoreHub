# 🌐 Web Client – ScoreHub

Preprosta spletna aplikacija (HTML + JS), ki prikazuje igralce, leaderboard in graf rezultatov.  
Povezana je z istim backend strežnikom kot desktop client.

---

## 🚀 Zagon
Odpri `index.html` v brskalniku.

Backend mora biti aktiven na:
http://127.0.0.1:5001

## 🔧 Funkcije
- Prikaz vseh igralcev (`GET /players`)
- Dodajanje novega igralca
- Leaderboard (razvrščeno po točkah)
- Graf rezultatov (Chart.js)
- Osnovni "quest log" za prikaz zadnjih akcij

## 📁 Struktura
web_client/
│── index.html
│── script.js
└── README.md

## 📝 Tehnologije
- HTML, CSS, JavaScript
- Chart.js za prikaz grafa
- Fetch API za komunikacijo z backendom


## ⚠️ Opombe
- Web client ne podpira herojev ali Card Battle (to je v desktop clientu).
- Deluje brez dodatnih knjižnic — ni potrebno poganjati serverja.