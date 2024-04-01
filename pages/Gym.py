from library import *
from services.Database import Database
from constants.Constants import *

st.set_page_config(layout="wide")

st.title("📁 Gym Dashboard")
st.markdown("You can see all information bellow!")

database = Database(worksheets=[
    ("GYM", 6)
])

# st.dataframe(database.worksheets["GYM"])

tab1, tab2 = st.tabs(["Analysis", "Register Fit"])

with tab1:
    ...

with tab2:
    date = st.date_input(label="Today")

    muscle_group = st.selectbox(label="Select Group Muscle", options=EXERCICES.keys())

    exercice = None
    if muscle_group != None:
        exercice = st.selectbox(label="Choice some exercise", options=EXERCICES[muscle_group])

    weight = st.number_input(label="Weight Value", step=1)
    
    series = st.selectbox(label="Choice a serie", options=SERIES)

    repetitions = st.selectbox(label="Choice a repetition size", options=REPETITIONS)