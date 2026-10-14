# NetflixScope — Exploratory Data Analysis of Netflix Movies & TV Shows

**Subject:** Advance Programming Lab-I (Python)  
**Subject Code:** CSE(AI/CPS/CS/DS)-3006

| Name              | Scholar No. |
|-------------------|-------------|
| Anupam Bichpuria  | 25U022014   |
| Ishu Nayak        | 25U022004   |

---

## Project Overview

NetflixScope is a comprehensive Exploratory Data Analysis (EDA) project that analyses the Netflix Movies and TV Shows dataset (`netflix_titles.csv`). The project includes:

1. **Jupyter Notebook** (`NetflixScope_EDA.ipynb`) — Full EDA with code, visualizations, and explanations.
2. **Word Report** (`NetflixScope_Report.docx`) — Academic-style report with charts and findings.
3. **Notebook Export** (`NetflixScope_EDA.html`) — HTML export of the executed notebook with all outputs.
4. **Interactive Dashboard** (`app.py`) — Streamlit + Plotly dashboard with filters and interactive charts.

## Setup

```bash
pip install -r requirements.txt
```

## Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## Project Structure

```
NetflixScope/
├── netflix_titles.csv          # Dataset (8,807 rows × 12 columns)
├── NetflixScope_EDA.ipynb      # Jupyter Notebook with full EDA
├── NetflixScope_Report.docx    # Word report
├── NetflixScope_EDA.html       # Notebook HTML export
├── app.py                      # Streamlit dashboard
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── charts/                     # Generated chart images (for report)
├── build_notebook.py           # Script to rebuild notebook
└── build_report.py             # Script to rebuild report
```

## Key Findings

- **Content Split:** Movies (~70%) significantly outnumber TV Shows (~30%).
- **Top Genres:** International Movies, Dramas, and Comedies dominate.
- **Top Countries:** United States and India are the leading content producers.
- **Growth:** Netflix expanded its library most aggressively between 2016–2019.
- **Ratings:** TV-MA is the most common rating, indicating adult-oriented content.
- **Duration:** Median movie length is ~100 minutes; most TV shows have only 1 season.

## Technologies Used

- Python 3.x
- Pandas, NumPy
- Matplotlib, Seaborn
- Streamlit, Plotly
- python-docx
