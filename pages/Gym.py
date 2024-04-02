from library import *
from services.Database import Database
from constants.Constants import *

st.set_page_config(layout="wide")

st.title("📁 Gym Dashboard")
st.markdown("You can input fit infomation bellow!")

database = Database(worksheets=[
    ("GYM", 12)
])

sheet = database.worksheets['GYM']

# st.dataframe(database.worksheets["GYM"])

tab1, tab2 = st.tabs(["Analysis", "Register Fit"])

with tab1:

    # division = st.selectbox(label="Select Division for Fit", options=DIVISION.keys())

    # for muscle in EXERCICES[division]:



    with st.expander("Dataframe"):
        st.data_editor(sheet)

with tab2:
    date = st.date_input(label="Today")

    muscle_group = st.selectbox(label="Select Group Muscle", options=EXERCICES.keys())

    exercice = None
    if muscle_group != None:
        exercice = st.selectbox(label="Choice some exercise", options=EXERCICES[muscle_group])

    series = st.selectbox(label="Choice a serie", options=SERIES)


    c1_rep, c2_rep = st.columns(2, gap="small")

    with c1_rep:
        repetitions = st.selectbox(label="Choice a repetition size", options=REPETITIONS)

    with c2_rep:
        drop_rep = st.toggle(label="Drop Repetition?")

        if drop_rep:
            weight = 0
            with st.expander("Drop Repetition:"):
                drop_rep_1 = st.number_input(label="Start Repetition", step=1)
                drop_rep_2 = st.number_input(label="Medium Repetition", step=1)
                drop_rep_3 = st.number_input(label="Last Repetition", step=1)
        else:
            drop_rep_1, drop_rep_2, drop_rep_3 = 0,0,0


    c1_weight, c2_weight = st.columns(2, gap="small")

    with c1_weight:
        weight = st.number_input(label="Weight Value", step=1)

    with c2_weight:
        drop_w = st.toggle(label="Drop Weight?")

        if drop_w:
            weight = 0
            with st.expander("Drop Weight:"):
                drop_w_1 = st.number_input(label="Start Weight", step=1)
                drop_w_2 = st.number_input(label="Medium Weight", step=1)
                drop_w_3 = st.number_input(label="Last Weight", step=1)
        else:
            drop_w_1, drop_w_2, drop_w_3 = 0,0,0


    submit_btn = st.button("Register")

    if submit_btn:
        if not muscle_group or not exercice or not series or not repetitions:
            st.warning("Fill all fields")
            st.stop()

        else:
            register_data = pd.DataFrame([{
                "Data": date.strftime('%d-%m-%Y'),
                "Grupo Muscular": muscle_group,
                "Exercicio": exercice,
                "Carga": weight,
                "Séries": series,
                "Repetições": repetitions,
                "Drop 1 - Carga": drop_w_1,
                "Drop 2 - Carga": drop_w_2,
                "Drop 3 - Carga": drop_w_3,
                "Drop 1 - Repetição": drop_rep_1,
                "Drop 2 - Repetição": drop_rep_2,
                "Drop 3 - Repetição": drop_rep_3,
            }])

            updated_df = pd.concat([sheet, register_data], ignore_index=True)

            database.conn.update(worksheet="GYM", data=updated_df)

            st.success("Fitness Registed with Success!")