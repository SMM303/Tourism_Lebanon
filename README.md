Lebanon Tourism Dashboard

This is a small Streamlit app I built for my Data Visualization and Communication course. It examines tourism across Lebanese towns using the Tourism Index and the number of hotels and guest houses in each town.

Live app: [add your Streamlit link here]

What the app shows

The page has two interactive charts. The first is a boxplot of the Tourism Index by area, split by whether a town has recorded tourism initiatives. The second is a bar chart of the 15 towns with the most accommodation (hotels and guest houses combined), coloured by Tourism Index.

Each chart comes with a short explanation and the key insights I drew from it.

How the filters work

There are two filters in the sidebar, and they are linked:

Select areas: pick one or more areas to compare.
Select towns: this list shows only towns within the areas you picked, so you can move from a broad view to specific towns. Leave it empty to see all towns in those areas.

The reasoning behind both filters is in the "Design justification" section at the top of the app.

Files
app.py: the Streamlit app
tourism.csv: the dataset
requirements.txt: the libraries needed to run it
Running it locally
bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

The app then opens in the browser at localhost:8501.
