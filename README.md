# Value Creation in Banking Industry
### M&A Mediobanca × Banca Generali — Analisi dei Multipli, Sinergie e Valutazione


> **[🔗 Visualizza la Dashboard Interattiva](https://YOUR_USERNAME.github.io/MA-Banking-Industry/)**

---

## 📌 Il Progetto

Questo lavoro analizza la **creazione di valore nel settore bancario italiano**, partendo da una diagnostica dei multipli di mercato delle principali banche quotate per arrivare alla valutazione dell'**OPS (Offerta Pubblica di Scambio) di Mediobanca su Banca Generali**.

L'analisi si sviluppa in **tre capitoli** interconnessi:

| # | Capitolo | Contenuto |
|---|----------|-----------|
| **01** | Capital Market Diagnostic | Analisi diagnostica dei multipli (P/E, P/BV) di 7 banche italiane (2022–2027E). Confronto tra gestori di risparmio, banche tradizionali e Mediobanca. |
| **02** | Drivers di Valutazione | Il ROTE come driver principale. Regressione OLS, gap di valutazione, leve strategiche per incrementare la redditività. |
| **03** | OPS su Banca Generali | Sinergie di ricavo, costo e funding. Re-rating dei multipli. Market cap stimata con tre scenari e analisi di sensitività. |

**Campione:** FinecoBank, Banca Generali, Banca Mediolanum, Mediobanca, Intesa Sanpaolo, UniCredit, Banco BPM

**Fonti:** FactSet, presentazione OPS Mediobanca (sezione investors)

---

## 📂 Struttura della Repo

```
MA-Banking-Industry/
│
├── index.html                          # Dashboard interattiva (GitHub Pages)
│
├── data/
│   ├── Dati_Banche.csv                 # Dataset principale (7 banche, 2022-2027E)
│   ├── Dati_Banche.xlsx                # Versione Excel del dataset
│   └── M_A_in_banking_industry.xlsx    # Workbook completo: analisi, sinergie, sensitività
│
├── analysis/
│   ├── M_A_Med_Gen.ipynb               # Jupyter Notebook — analisi completa
│   ├── M_A_Med_Gen.py                  # Script Python standalone
│   └── M_A_Med_Gen.html               # Export HTML del notebook (con output)
│
├── dashboard/
│   └── M_A_Med_Gen_Dashboard_v2.html   # Copia della dashboard
│
├── docs/
│   └── preview.png                     # Screenshot per il README
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Visualizzare la Dashboard

Il modo più semplice: apri `index.html` nel browser (doppio click).

Oppure con VS Code:
1. Installa l'estensione [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
2. Click destro su `index.html` → **Open with Live Server**

### Eseguire l'Analisi Python

```bash
# Clona la repo
git clone https://github.com/YOUR_USERNAME/MA-Banking-Industry.git
cd MA-Banking-Industry

# Installa le dipendenze
pip install -r requirements.txt

# Esegui lo script
python analysis/M_A_Med_Gen.py

# Oppure apri il notebook
jupyter notebook analysis/M_A_Med_Gen.ipynb
```

---

## 🌐 Pubblicare la Dashboard con GitHub Pages

Per rendere la dashboard accessibile a chiunque tramite un link:

1. **Vai su GitHub** → Settings della repo → **Pages**
2. Sotto "Source" seleziona **Deploy from a branch**
3. Seleziona il branch `main` e la cartella `/ (root)`
4. Clicca **Save**

Dopo qualche minuto la dashboard sarà live a:
```
https://YOUR_USERNAME.github.io/MA-Banking-Industry/
```

> ⚠️ Ricorda di sostituire `YOUR_USERNAME` con il tuo username GitHub nel link del README.

---

## 📊 Risultati Chiave

| Metrica | Pre-OPS | Post-OPS |
|---------|---------|----------|
| ROTE | 12.4% | >20% |
| P/E | 10.2x | **12.4x** |
| Incidenza WM su ricavi | 26% | 45% |
| Incidenza WM su utile | <20% | 50% |
| TFA | — | >€210B |
| CET1 | ~15% | ~14% |

| Scenario | Sinergie Totali 2028 | Net Income Diff. | ΔMarket Cap |
|----------|---------------------|------------------|-------------|
| Pessimistic | ~€120K | ~€50K | +€3.3B |
| **Baseline** | **€300K** | **€248K** | **+€5.7B** |
| Optimistic | ~€480K | ~€400K | +€8.3B |

---

## 🛠️ Tech Stack

- **Dashboard:** HTML/CSS/JS vanilla + [Chart.js](https://www.chartjs.org/) + Google Fonts
- **Analisi:** Python (pandas, numpy, matplotlib, statsmodels)
- **Dati:** FactSet, presentazione OPS Mediobanca

---

## 📄 License

Questo progetto è a scopo didattico e di ricerca. I dati finanziari sono di fonte pubblica (FactSet, presentazioni societarie).
