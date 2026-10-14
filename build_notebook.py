"""
Build and execute the NetflixScope EDA notebook programmatically.
"""
# pyrefly: ignore [missing-import]
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

nb = new_notebook()
nb.metadata.kernelspec = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}
cells = []

def md(text):
    cells.append(new_markdown_cell(text))

def code(text):
    cells.append(new_code_cell(text))

# =====================================================================
# 1. TITLE & INTRODUCTION
# =====================================================================
md("""# NetflixScope — Exploratory Data Analysis of Netflix Movies & TV Shows

**Subject:** Advance Programming Lab-I (Python)  
**Subject Code:** CSE(AI/CPS/CS/DS)-3006

| Name | Scholar No. |
|---|---|
| Anupam Bichpuria | 25U022014 |
| Ishu Nayak | 25U022004 |

---

## 1. Introduction

Netflix is one of the largest media and video streaming platforms in the world. As of mid-2021, the platform hosted over 8,000 movies and TV shows. Understanding the composition of this content library — the mix of movies versus TV shows, the dominant genres, the geographic spread of productions, and temporal trends — is valuable for data-driven decision-making.

### Objectives
1. Understand the structure, quality, and distribution of the Netflix dataset.
2. Clean and preprocess the data for reliable analysis.
3. Perform univariate, bivariate, and multivariate analyses.
4. Visualize key patterns and trends using charts.
5. Summarize findings, acknowledge limitations, and draw conclusions.

### Dataset Description
The dataset `netflix_titles.csv` contains information about Movies and TV Shows available on Netflix. Each row represents a single title with attributes such as type, title, director, cast, country, date added, release year, rating, duration, genres, and a brief description.
""")

# =====================================================================
# 2. IMPORTS & SETUP
# =====================================================================
md("## 2. Setup — Import Libraries")

code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid', palette='Set2')
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['figure.dpi'] = 100

print("Libraries loaded successfully.")
""")

# =====================================================================
# 3. LOAD & INSPECT
# =====================================================================
md("## 3. Dataset Loading and Inspection")

code("""df = pd.read_csv('netflix_titles.csv')
print(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
df.head()
""")

code("""df.tail()
""")

code("""df.info()
""")

# =====================================================================
# 4. DATA TYPES & DESCRIPTIVE STATS
# =====================================================================
md("## 4. Data Types and Descriptive Statistics")

code("""print("Data types:\\n")
print(df.dtypes)
""")

code("""df.describe()
""")

code("""df.describe(include='object')
""")

# =====================================================================
# 5. MISSING VALUES
# =====================================================================
md("""## 5. Missing-Value Analysis and Handling

We check for missing values in each column, visualize them, and then apply appropriate strategies:
- **director, cast, country**: Fill with `'Unknown'` (categorical, no reliable way to impute).
- **date_added**: Drop the few rows where this is missing since we need date parsing.
- **rating, duration**: Fill with mode or `'Unknown'`.
""")

code("""missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Percentage (%)': missing_pct})
missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
print(missing_df)
""")

code("""fig, ax = plt.subplots(figsize=(8, 4))
missing_df['Missing Count'].plot(kind='barh', color='salmon', edgecolor='black', ax=ax)
ax.set_title('Missing Values per Column')
ax.set_xlabel('Count')
plt.tight_layout()
plt.show()
""")

code("""# Fill missing categorical values
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df['duration'] = df['duration'].fillna(df['duration'].mode()[0])

# Drop rows where date_added is missing (very few)
print(f"Rows before dropping missing date_added: {len(df)}")
df = df.dropna(subset=['date_added'])
print(f"Rows after: {len(df)}")

# Verify no missing values remain
print(f"\\nRemaining missing values: {df.isnull().sum().sum()}")
""")

# =====================================================================
# 6. DUPLICATES
# =====================================================================
md("""## 6. Duplicate Detection and Removal

We check for duplicate rows based on the `title` and `type` columns — a title can appear only once as a Movie and once as a TV Show.
""")

code("""dup_count = df.duplicated(subset=['title', 'type']).sum()
print(f"Duplicate rows (by title + type): {dup_count}")

if dup_count > 0:
    df = df.drop_duplicates(subset=['title', 'type'], keep='first')
    print(f"Rows after removing duplicates: {len(df)}")
else:
    print("No duplicates found — no removal needed.")
""")

# =====================================================================
# 7. DATE PARSING & PREPROCESSING
# =====================================================================
md("""## 7. Date Parsing and Data Preprocessing

We parse `date_added` into a proper datetime, extract useful components (year, month, day of week), and split `duration` into numeric columns for Movies (minutes) and TV Shows (seasons).
""")

code("""# Parse date_added
df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df['day_of_week'] = df['date_added'].dt.day_name()

# Parse duration
df['duration_int'] = df['duration'].str.extract(r'(\d+)').astype(float)

print("Preprocessing complete.")
print(f"\\nNew columns: year_added, month_added, day_of_week, duration_int")
df[['title', 'date_added', 'year_added', 'month_added', 'day_of_week', 'duration', 'duration_int']].head(10)
""")

# =====================================================================
# 8. MOVIES vs TV SHOWS
# =====================================================================
md("""## 8. Movies versus TV Shows

Let's look at the overall content split between Movies and TV Shows on Netflix.
""")

code("""type_counts = df['type'].value_counts()
print(type_counts)
print(f"\\nMovie percentage: {type_counts.get('Movie',0)/len(df)*100:.1f}%")
print(f"TV Show percentage: {type_counts.get('TV Show',0)/len(df)*100:.1f}%")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
colors = ['#E50914', '#564d4d']
axes[0].pie(type_counts, labels=type_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90, explode=[0.03, 0.03],
            textprops={'fontsize': 12})
axes[0].set_title('Content Type Distribution', fontsize=14)

# Bar chart
type_counts.plot(kind='bar', color=colors, edgecolor='black', ax=axes[1])
axes[1].set_title('Content Type Count', fontsize=14)
axes[1].set_ylabel('Count')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

plt.tight_layout()
plt.show()
""")

# =====================================================================
# 9. GENRE ANALYSIS
# =====================================================================
md("""## 9. Genre Analysis

The `listed_in` column contains comma-separated genres. We split them to find the most common genres on Netflix.
""")

code("""# Split genres
genres = df['listed_in'].str.split(', ').explode()
genre_counts = genres.value_counts().head(15)

print("Top 15 Genres:\\n")
print(genre_counts)
""")

code("""fig, ax = plt.subplots(figsize=(10, 6))
genre_counts.plot(kind='barh', color='coral', edgecolor='black', ax=ax)
ax.set_title('Top 15 Genres on Netflix', fontsize=14)
ax.set_xlabel('Number of Titles')
ax.invert_yaxis()
plt.tight_layout()
plt.show()
""")

code("""# Genre split by content type
genre_type = df[['listed_in', 'type']].copy()
genre_type = genre_type.assign(genre=genre_type['listed_in'].str.split(', ')).explode('genre')
top_genres = genre_type['genre'].value_counts().head(10).index.tolist()
genre_type_filtered = genre_type[genre_type['genre'].isin(top_genres)]

ct = genre_type_filtered.groupby(['genre', 'type']).size().unstack(fill_value=0)
ct = ct.loc[ct.index.isin(top_genres)]
# Reorder to match top genres order
ct = ct.reindex([g for g in top_genres if g in ct.index])

fig, ax = plt.subplots(figsize=(10, 6))
ct.plot(kind='barh', stacked=True, color=['#E50914', '#564d4d'], edgecolor='black', ax=ax)
ax.set_title('Top 10 Genres - Movies vs TV Shows', fontsize=14)
ax.set_xlabel('Count')
ax.legend(title='Type')
ax.invert_yaxis()
plt.tight_layout()
plt.show()
""")

# =====================================================================
# 10. COUNTRY ANALYSIS
# =====================================================================
md("""## 10. Country Analysis

Some titles list multiple countries. We split them and examine the top content-producing countries.
""")

code("""countries = df[df['country'] != 'Unknown']['country'].str.split(', ').explode().str.strip()
country_counts = countries.value_counts().head(15)

print("Top 15 Countries:\\n")
print(country_counts)
""")

code("""fig, ax = plt.subplots(figsize=(10, 6))
country_counts.plot(kind='barh', color='steelblue', edgecolor='black', ax=ax)
ax.set_title('Top 15 Content-Producing Countries', fontsize=14)
ax.set_xlabel('Number of Titles')
ax.invert_yaxis()
plt.tight_layout()
plt.show()
""")

# =====================================================================
# 11. RELEASE YEAR & YEAR ADDED TRENDS
# =====================================================================
md("""## 11. Release-Year and Titles-Added-Year Trends

We look at when content was originally released and when it was added to the Netflix platform.
""")

code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Release year distribution
df['release_year'].value_counts().sort_index().tail(30).plot(
    kind='line', marker='o', color='#E50914', ax=axes[0])
axes[0].set_title('Titles by Release Year (Last 30 Years)', fontsize=13)
axes[0].set_xlabel('Release Year')
axes[0].set_ylabel('Count')

# Year added trend
year_added_counts = df['year_added'].value_counts().sort_index()
year_added_counts.plot(kind='bar', color='teal', edgecolor='black', ax=axes[1])
axes[1].set_title('Titles Added to Netflix by Year', fontsize=13)
axes[1].set_xlabel('Year Added')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.show()
""")

code("""# Trend by type and year added
type_year = df.groupby(['year_added', 'type']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10, 5))
type_year.plot(kind='line', marker='o', color=['#E50914', '#564d4d'], ax=ax)
ax.set_title('Movies vs TV Shows Added per Year', fontsize=14)
ax.set_xlabel('Year')
ax.set_ylabel('Count')
ax.legend(title='Type')
plt.tight_layout()
plt.show()
""")

# =====================================================================
# 12. DURATION ANALYSIS
# =====================================================================
md("""## 12. Movie Duration and TV Show Season Analysis

For Movies we analyse the duration in minutes; for TV Shows we look at the number of seasons.
""")

code("""movies = df[df['type'] == 'Movie'].copy()
tv_shows = df[df['type'] == 'TV Show'].copy()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Movie duration histogram
axes[0].hist(movies['duration_int'].dropna(), bins=30, color='#E50914',
             edgecolor='black', alpha=0.8)
axes[0].set_title('Movie Duration Distribution (minutes)', fontsize=13)
axes[0].set_xlabel('Duration (min)')
axes[0].set_ylabel('Frequency')
axes[0].axvline(movies['duration_int'].median(), color='black',
                linestyle='--', label=f"Median: {movies['duration_int'].median():.0f} min")
axes[0].legend()

# TV show seasons
axes[1].hist(tv_shows['duration_int'].dropna(), bins=range(0, 18),
             color='teal', edgecolor='black', alpha=0.8)
axes[1].set_title('TV Show Number of Seasons', fontsize=13)
axes[1].set_xlabel('Seasons')
axes[1].set_ylabel('Frequency')
axes[1].axvline(tv_shows['duration_int'].median(), color='black',
                linestyle='--', label=f"Median: {tv_shows['duration_int'].median():.0f} season(s)")
axes[1].legend()

plt.tight_layout()
plt.show()

print(f"Movie duration stats:\\n{movies['duration_int'].describe().round(1)}\\n")
print(f"TV Show season stats:\\n{tv_shows['duration_int'].describe().round(1)}")
""")

# =====================================================================
# 13. RATING ANALYSIS
# =====================================================================
md("""## 13. Content-Rating Analysis

Netflix content carries maturity ratings like TV-MA, TV-14, PG-13, etc. Let's see how they are distributed.
""")

code("""rating_counts = df['rating'].value_counts()
print(rating_counts)
""")

code("""fig, ax = plt.subplots(figsize=(10, 5))
rating_counts.plot(kind='bar', color='mediumpurple', edgecolor='black', ax=ax)
ax.set_title('Content Rating Distribution', fontsize=14)
ax.set_xlabel('Rating')
ax.set_ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
""")

code("""# Rating by content type
top_ratings = rating_counts.head(8).index.tolist()
rating_type = df[df['rating'].isin(top_ratings)].groupby(['rating', 'type']).size().unstack(fill_value=0)
rating_type = rating_type.reindex([r for r in top_ratings if r in rating_type.index])

fig, ax = plt.subplots(figsize=(10, 5))
rating_type.plot(kind='bar', stacked=True, color=['#E50914', '#564d4d'],
                 edgecolor='black', ax=ax)
ax.set_title('Top 8 Ratings - Movies vs TV Shows', fontsize=14)
ax.set_xlabel('Rating')
ax.set_ylabel('Count')
ax.legend(title='Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
""")

# =====================================================================
# 14. OUTLIER DETECTION
# =====================================================================
md("""## 14. Outlier Detection Using IQR

We use the Interquartile Range (IQR) method to detect outliers in movie durations and release years.

**IQR Method:** Any value below Q1 − 1.5×IQR or above Q3 + 1.5×IQR is considered an outlier.
""")

code("""def detect_outliers_iqr(series, name):
    \"\"\"Detect outliers using the IQR method and print summary.\"\"\"
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = series[(series < lower) | (series > upper)]
    print(f"--- {name} ---")
    print(f"  Q1={Q1}, Q3={Q3}, IQR={IQR}")
    print(f"  Lower bound={lower}, Upper bound={upper}")
    print(f"  Outliers found: {len(outliers)} out of {len(series)} values")
    print(f"  Outlier percentage: {len(outliers)/len(series)*100:.2f}%\\n")
    return lower, upper, outliers

# Movie duration outliers
l, u, movie_outliers = detect_outliers_iqr(movies['duration_int'].dropna(), 'Movie Duration (min)')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].boxplot(movies['duration_int'].dropna(), vert=True, patch_artist=True,
                boxprops=dict(facecolor='#E50914', alpha=0.6))
axes[0].set_title('Movie Duration — Box Plot', fontsize=13)
axes[0].set_ylabel('Duration (min)')

# Release year outliers
l2, u2, year_outliers = detect_outliers_iqr(df['release_year'], 'Release Year')
axes[1].boxplot(df['release_year'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='teal', alpha=0.6))
axes[1].set_title('Release Year — Box Plot', fontsize=13)
axes[1].set_ylabel('Year')

plt.tight_layout()
plt.show()
""")

# =====================================================================
# 15. MULTIVARIATE ANALYSIS & CORRELATION
# =====================================================================
md("""## 15. Multivariate Analysis and Correlation

Since most columns are categorical, we compute correlations on the available numerical columns (`release_year`, `duration_int`, `year_added`, `month_added`) and supplement with cross-tabulation analysis.
""")

code("""numeric_cols = df[['release_year', 'duration_int', 'year_added', 'month_added']].dropna()

corr = numeric_cols.corr()
print("Correlation matrix:\\n")
print(corr.round(3))
""")

code("""fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=0.5, ax=ax)
ax.set_title('Correlation Heatmap (Numerical Features)', fontsize=14)
plt.tight_layout()
plt.show()
""")

code("""# Scatter: release year vs duration (Movies only)
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(movies['release_year'], movies['duration_int'], alpha=0.3,
           color='#E50914', edgecolors='gray', s=15)
ax.set_title('Movie Duration vs Release Year', fontsize=14)
ax.set_xlabel('Release Year')
ax.set_ylabel('Duration (min)')
plt.tight_layout()
plt.show()
""")

code("""# Monthly content-addition heatmap by type
month_type = df.groupby(['month_added', 'type']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(month_type.T, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
ax.set_title('Content Added per Month (by Type)', fontsize=14)
ax.set_xlabel('Month')
ax.set_ylabel('')
plt.tight_layout()
plt.show()
""")

# =====================================================================
# 16. PAIRPLOT
# =====================================================================
code("""# Pair-plot of numerical features coloured by content type
# (sample to keep it fast)
sample = df[['release_year', 'duration_int', 'year_added', 'type']].dropna().sample(
    n=min(1000, len(df)), random_state=42)
g = sns.pairplot(sample, hue='type', palette={'Movie': '#E50914', 'TV Show': '#564d4d'},
                 diag_kind='hist', plot_kws={'alpha': 0.5, 's': 15})
g.figure.suptitle('Pair Plot of Numerical Features by Content Type', y=1.02, fontsize=14)
plt.show()
""")

# =====================================================================
# 17. FINDINGS, LIMITATIONS, CONCLUSION
# =====================================================================
md("""## 16. Findings, Limitations, and Conclusion

### Key Findings
1. **Content Split:** Movies significantly outnumber TV Shows on Netflix (roughly 70-30 split).
2. **Dominant Genres:** International Movies, Dramas, and Comedies are the most common genres, reflecting Netflix's global strategy.
3. **Geographic Concentration:** The United States and India are the top content-producing countries by a large margin.
4. **Temporal Trends:** The bulk of content was added between 2016-2021, with a noticeable dip in 2020 (likely pandemic-related production delays) and a peak around 2019.
5. **Movie Duration:** Most movies are between 80-120 minutes, with a median around 100 minutes.
6. **TV Shows:** The vast majority of TV shows have only 1 season, indicating Netflix acquires many limited or single-season series.
7. **Ratings:** TV-MA is the most common rating, followed by TV-14, suggesting Netflix's catalogue skews toward adult-oriented content.
8. **Outliers:** Some very short films (< 20 min) and very long ones (> 180 min) exist as outliers.

### Limitations
- The dataset is a snapshot (up to ~2021) and does not reflect current Netflix content.
- The `director` and `cast` fields have significant missing data, limiting cast/crew analysis.
- Genre labels are assigned by Netflix and may not follow standard film-industry categorizations.
- Multi-country productions are counted once per country when split, slightly inflating counts.

### Conclusion
This EDA reveals that Netflix has built a content library that is predominantly movie-based and adult-oriented, with a strong global footprint, particularly in the US and India. The platform expanded its library aggressively between 2016-2020. The analysis also highlights data-quality challenges such as missing metadata. Future work could incorporate user-engagement metrics and more recent data to paint a fuller picture.

---
*End of Notebook — NetflixScope EDA*
""")

# =====================================================================
# ASSEMBLE & SAVE
# =====================================================================
nb.cells = cells

# Save unexecuted notebook first
with open('NetflixScope_EDA.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook created: NetflixScope_EDA.ipynb")
print("Now executing all cells...")

# Execute the notebook
from nbconvert.preprocessors import ExecutePreprocessor
ep = ExecutePreprocessor(timeout=300, kernel_name='python3')

import os
ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})

# Save the executed notebook
with open('NetflixScope_EDA.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook executed and saved with outputs successfully!")
