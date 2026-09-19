import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px

# Page settings (must be the first Streamlit command, and only called once)
st.set_page_config(page_title="Lebanon Tourism", layout="wide")
BASE_DIR = Path(__file__).parent

# ---------------------------------------------------------------
# SETTINGS: file name and column names
# ---------------------------------------------------------------
DATA_FILE = BASE_DIR / "tourism.csv"
COL_AREA = "refArea"
COL_TOWN = "Town"
COL_INDEX = "Tourism Index"
COL_INITIATIVE = "Existence of initiatives and projects in the past five years to improve the tourism sector - exists"
COL_HOTELS = "Total number of hotels"
COL_GUEST = "Total number of guest houses"


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)

    missing = [c for c in [COL_AREA, COL_TOWN, COL_INDEX, COL_INITIATIVE, COL_HOTELS, COL_GUEST]
               if c not in df.columns]
    if missing:
        return df, missing

    # Turn area links such as ".../Akkar_Governorate" into "Akkar Governorate"
    df[COL_AREA] = (
        df[COL_AREA].astype(str).str.split("/").str[-1].str.replace("_", " ").str.strip()
    )
    df["Accommodation"] = df[COL_HOTELS].fillna(0) + df[COL_GUEST].fillna(0)
    df["Initiatives"] = df[COL_INITIATIVE].apply(
        lambda v: "With initiatives" if v == 1 else "Without initiatives"
    )
    return df, []


if not DATA_FILE.exists():
    st.error(f"Data file not found: {DATA_FILE.name}. Put it in the same folder as app.py.")
    st.stop()

df, missing = load_data(DATA_FILE)
if missing:
    st.error(f"These columns were not found: {missing}")
    st.write("Columns in your file:", list(df.columns))
    st.stop()

# ---------------------------------------------------------------
# LINKED FILTERS
# ---------------------------------------------------------------
st.sidebar.header("Filters")

areas = sorted(df[COL_AREA].dropna().unique())
selected_areas = st.sidebar.multiselect("1. Select areas", areas, default=areas)

# Town options depend on the areas chosen above
area_df = df[df[COL_AREA].isin(selected_areas)]
towns = sorted(area_df[COL_TOWN].dropna().unique())
selected_towns = st.sidebar.multiselect(
    "2. Select towns (leave empty for all towns in the chosen areas)", towns
)

filtered = area_df[area_df[COL_TOWN].isin(selected_towns)] if selected_towns else area_df

st.sidebar.markdown(f"**Towns shown:** {filtered[COL_TOWN].nunique()}")

# ---------------------------------------------------------------
# PAGE CONTENT
# ---------------------------------------------------------------
st.title("Lebanon Tourism")
st.write(
    "This page presents tourism performance and accommodation capacity across "
    "areas and towns in Lebanon. Use the filters in the sidebar to focus on "
    "specific areas, then on specific towns within them."
)

with st.expander("Design justification: how the filters work and why"):
    st.markdown("#### Feature 1: Area multiselect")
    st.markdown(
        "This filter helps answering the question: how do tourism "
        "performance and accommodation capacity differ between the areas of "
        "Lebanon that matter to me? A multiselect was used instead of a "
        "selectbox because the user needs to compare two or more areas at once, "
        "such as Akkar and Nabatieh, which a selectbox does not allow. "
        "Checkboxes were also considered but not used, since a full list of "
        "boxes would add clutter to the sidebar. The filter applies the course "
        "principle of reducing clutter by removing irrelevant areas from the "
        "boxplot and bar chart comparisons."
    )

    st.markdown("#### Feature 2: Town multiselect, linked to the area filter")
    st.markdown(
        "This filter helps answering the question: within the areas I "
        "selected, which towns stand out, and how do they compare? Its options "
        "depend on the first filter, so it lists only the towns that belong to "
        "the selected areas. An independent town list was considered, but it "
        "would display every town in the dataset, make the required towns hard "
        "to find, and allow users to select contradictory combinations that "
        "return empty charts. A multiselect was chosen instead of a slider or "
        "text field because towns are categorical rather than numerical data. "
        "The filter applies the course concept of focusing attention: the user "
        "moves from an overview of areas to a subset of towns, following the "
        "pattern of overview first, zoom and filter, then details on demand."
    )

if filtered.empty:
    st.warning("No data for this selection. Choose at least one area.")
    st.stop()

# Chart 1: Tourism Index distribution
st.header("Index Distribution Across Areas")
fig1 = px.box(
    filtered, x=COL_AREA, y=COL_INDEX, color="Initiatives", points="outliers",
    labels={COL_AREA: "Area", COL_INDEX: "Tourism Index"},
)
st.plotly_chart(fig1)

st.subheader("Explanation")
st.markdown(
    "The Tourism Index is numeric but repeated across many towns, so a boxplot "
    "showing spread, median, and outliers is more informative than a bar chart "
    "of raw values."
)

st.subheader("Key Insights")
st.caption("Insights below describe the full dataset.")
st.markdown(
    "Areas with initiatives generally record a higher median Tourism Index than "
    "those without, most visibly in Sidon, Nabatieh, and Akkar."
)
st.markdown(
    "South and Beqaa show the widest spread, pointing to uneven development "
    "within a single governorate."
)
st.markdown(
    "Outlier towns appear even where no initiative is recorded, marking "
    "candidates worth closer attention."
)

# Chart 2: Accommodation capacity
st.header("Accommodation Capacity Across the Leading Towns")
top = filtered.nlargest(15, "Accommodation")
fig2 = px.bar(
    top, x=COL_TOWN, y="Accommodation", color=COL_INDEX,
    color_continuous_scale="Viridis",
    labels={COL_TOWN: "Town", "Accommodation": "Hotels + guest houses",
            COL_INDEX: "Tourism Index"},
)
st.plotly_chart(fig2)

st.subheader("Explanation")
st.markdown(
    "Bar height shows the town’s accommodation infrastructure, measured as the "
    "combined number of hotels and guest houses. Colour represents the Tourism "
    "Index. Towns with the same Tourism Index, such as TI 10 or TI 9, appear in "
    "the same or very similar shade."
)

st.subheader("Key Insights")
st.caption("Insights below describe the full dataset.")
st.markdown(
    "Bqerqacha, Zgharta-Ehden, and Bcharreh lead by a wide margin, showing the "
    "strongest accommodation capacity when hotels and guest houses are combined."
)
st.markdown(
    "Including guest houses gives a more complete picture of tourism "
    "infrastructure, especially for towns where visitor accommodation is not "
    "limited to hotels only."
)
st.markdown(
    "Colour is useful for linking infrastructure to tourism performance, but it "
    "becomes less distinctive when several towns share the same Tourism Index value."
)