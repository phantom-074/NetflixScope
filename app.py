"""
NetflixScope Dashboard — Streamlit + Plotly
A simple, dark-themed interactive dashboard for Netflix EDA.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="NetflixScope Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS — dark theme with red accents ─────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #141414;
        color: #e5e5e5;
    }
    .stSidebar > div:first-child {
        background-color: #1a1a2e;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #E50914;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #E50914;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #b3b3b3;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    h1, h2, h3 {
        color: #e5e5e5 !important;
    }
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #e5e5e5 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
    df['duration'] = df['duration'].fillna(df['duration'].mode()[0])
    df = df.dropna(subset=['date_added'])
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['duration_int'] = df['duration'].str.extract(r'(\d+)').astype(float)
    return df

df = load_data()

# ── Plotly template ──────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"
RED = "#E50914"
DARK_BG = "#141414"
CARD_BG = "#1a1a2e"

# ── Sidebar filters ─────────────────────────────────────────────────
st.sidebar.markdown("## 🎬 NetflixScope")
st.sidebar.markdown("---")

# Content type filter
content_type = st.sidebar.selectbox(
    "Content Type",
    options=["All", "Movie", "TV Show"]
)

# Country filter
all_countries = sorted(
    df[df['country'] != 'Unknown']['country']
    .str.split(', ').explode().str.strip().unique()
)
selected_countries = st.sidebar.multiselect(
    "Country",
    options=all_countries,
    default=[]
)

# Release year filter
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider(
    "Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Rating filter
all_ratings = sorted(df['rating'].dropna().unique())
selected_ratings = st.sidebar.multiselect(
    "Rating",
    options=all_ratings,
    default=[]
)

# ── Apply filters ────────────────────────────────────────────────────
filtered = df.copy()
if content_type != "All":
    filtered = filtered[filtered['type'] == content_type]
if selected_countries:
    mask = filtered['country'].apply(
        lambda x: any(c in x for c in selected_countries)
    )
    filtered = filtered[mask]
filtered = filtered[
    (filtered['release_year'] >= year_range[0]) &
    (filtered['release_year'] <= year_range[1])
]
if selected_ratings:
    filtered = filtered[filtered['rating'].isin(selected_ratings)]

# ── Header ───────────────────────────────────────────────────────────
st.markdown("# 🎬 NetflixScope Dashboard")
st.markdown("*Exploratory Data Analysis of Netflix Movies & TV Shows*")
st.markdown("---")

# ── KPI Cards ────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

movies_count = len(filtered[filtered['type'] == 'Movie'])
tvshows_count = len(filtered[filtered['type'] == 'TV Show'])
countries_count = filtered[filtered['country'] != 'Unknown']['country'].str.split(', ').explode().str.strip().nunique()
genres_count = filtered['listed_in'].str.split(', ').explode().nunique()

kpis = [
    (k1, str(len(filtered)), "Total Titles"),
    (k2, str(movies_count), "Movies"),
    (k3, str(tvshows_count), "TV Shows"),
    (k4, str(countries_count), "Countries"),
    (k5, str(genres_count), "Genres"),
]

for col, value, label in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{value}</p>
            <p class="kpi-label">{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ── Row 1: Content Type + Top Genres ─────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    type_counts = filtered['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig = px.pie(type_counts, values='Count', names='Type',
                 color='Type',
                 color_discrete_map={'Movie': RED, 'TV Show': '#564d4d'},
                 template=PLOTLY_TEMPLATE,
                 title='Content Type Distribution')
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                      font_color='#e5e5e5')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    genres = filtered['listed_in'].str.split(', ').explode()
    genre_counts = genres.value_counts().head(12).reset_index()
    genre_counts.columns = ['Genre', 'Count']
    fig = px.bar(genre_counts, x='Count', y='Genre', orientation='h',
                 color_discrete_sequence=[RED],
                 template=PLOTLY_TEMPLATE,
                 title='Top 12 Genres')
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                      font_color='#e5e5e5', yaxis=dict(autorange='reversed'))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Countries + Yearly Trends ────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    country_data = filtered[filtered['country'] != 'Unknown']['country'].str.split(', ').explode().str.strip()
    country_counts = country_data.value_counts().head(12).reset_index()
    country_counts.columns = ['Country', 'Count']
    fig = px.bar(country_counts, x='Count', y='Country', orientation='h',
                 color_discrete_sequence=['#0077b6'],
                 template=PLOTLY_TEMPLATE,
                 title='Top 12 Countries')
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                      font_color='#e5e5e5', yaxis=dict(autorange='reversed'))
    st.plotly_chart(fig, use_container_width=True)

with c4:
    yearly = filtered.groupby(['year_added', 'type']).size().reset_index(name='Count')
    fig = px.line(yearly, x='year_added', y='Count', color='type',
                  color_discrete_map={'Movie': RED, 'TV Show': '#564d4d'},
                  template=PLOTLY_TEMPLATE,
                  title='Content Added per Year',
                  markers=True)
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                      font_color='#e5e5e5',
                      xaxis_title='Year', yaxis_title='Titles Added')
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Duration + Ratings ────────────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    if content_type in ("All", "Movie"):
        movie_data = filtered[filtered['type'] == 'Movie']['duration_int'].dropna()
        if len(movie_data) > 0:
            fig = px.histogram(movie_data, nbins=30,
                               color_discrete_sequence=[RED],
                               template=PLOTLY_TEMPLATE,
                               title='Movie Duration Distribution (min)',
                               labels={'value': 'Duration (min)', 'count': 'Frequency'})
            fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                              font_color='#e5e5e5', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    if content_type == "TV Show":
        tv_data = filtered[filtered['type'] == 'TV Show']['duration_int'].dropna()
        if len(tv_data) > 0:
            fig = px.histogram(tv_data, nbins=15,
                               color_discrete_sequence=['#0077b6'],
                               template=PLOTLY_TEMPLATE,
                               title='TV Show Seasons Distribution',
                               labels={'value': 'Seasons', 'count': 'Frequency'})
            fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                              font_color='#e5e5e5', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

with c6:
    rating_counts = filtered['rating'].value_counts().head(10).reset_index()
    rating_counts.columns = ['Rating', 'Count']
    fig = px.bar(rating_counts, x='Rating', y='Count',
                 color_discrete_sequence=['#7b2cbf'],
                 template=PLOTLY_TEMPLATE,
                 title='Top 10 Content Ratings')
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                      font_color='#e5e5e5')
    st.plotly_chart(fig, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666;'>"
    "NetflixScope — Anupam Bichpuria (25U022014) & Ishu Nayak (25U022004) "
    "| Advance Programming Lab-I (Python) | CSE(AI/CPS/CS/DS)-3006"
    "</div>",
    unsafe_allow_html=True
)
