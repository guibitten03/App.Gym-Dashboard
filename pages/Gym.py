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

    c1, c2 = st.columns(2, gap="small")

    with c1:
        weight = st.number_input(label="Weight Value", step=1)

    with c2:
        drop = st.toggle(label="Drop?")

        if drop:
            weight = 0
            with st.expander("Drop Weight:"):
                drop1 = st.number_input(label="Start Weight")
                drop2 = st.number_input(label="Medium Weight")
                drop3 = st.number_input(label="Last Weight")
        else:
            drop1, drop2, drop3 = 0,0,0


    series = st.selectbox(label="Choice a serie", options=SERIES)

    repetitions = st.selectbox(label="Choice a repetition size", options=REPETITIONS)

    submit_btn = st.button("Register")

    # if submit_btn:
    #     if not muscle_group or not exercice or not weight or not series or not repetitions:
    #         st.warning("Fill all fields")
    #         st.stop()

    #     else:
