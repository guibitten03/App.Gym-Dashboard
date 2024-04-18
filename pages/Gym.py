from library import *
from services.Database import Database
import streamlit_card as st_card 

from constants.Constants import *

st.set_page_config(layout="wide")

st.title("📁 Gym Dashboard")
st.markdown("You can input fit infomation bellow!")

database = Database(worksheets=[
    ("GYM", 12),
    ("TRAINS", 8)
])

gym = database.worksheets['GYM']
trains = database.worksheets['TRAINS']

# st.dataframe(database.worksheets["GYM"])

tab1, tab2, tab3 = st.tabs(["Current Train", "Register Fit", "Register Train"])

with tab1:

    division = st.selectbox(label="Select Today Fit", options=DIVISION.keys())

    st.divider()

    exercicies_muscle = trains.loc[trains['Division Train'] == division].iloc[:, 1:]

    exercicies_muscle_dict = exercicies_muscle.to_dict()

    titles = exercicies_muscle_dict['Muscle Group'].values()

    for group in titles:
        st.markdown(f"### {group.upper()}")

        train_pattern = trains.loc[trains["Muscle Group"] == group]

        ex_list = [i for i in train_pattern.values.tolist()[0] if str(i) != '*'][2:]  

        n_cols = len(ex_list)
        cols = st.columns(n_cols, gap="small")

        for col, ex in zip(cols, ex_list):
            if ex not in gym['Exercicio'].values:
                continue

            ex_status = gym.loc[gym['Exercicio'] == ex].tail(1)

            with col:
                with st.container(border=True):
                    st.markdown(f'''
                                #### {ex}
                                ##### {int(ex_status['Carga'].values)} Kg. | {int(ex_status['Repetições'].values)} Rep. | {int(ex_status['Séries'].values)} Ser.
                                ''')

        st.divider()            


    with st.expander("Dataframe"):
        gym_edition = st.data_editor(gym)

        submit_editor = st.button(label="Update Dataframe")

        if submit_editor:
            database.conn.update(worksheet="GYM", data=gym_edition)

            st.success("Fitness Registed with Success!")



with tab2:

    with st.container(border=True):
        date = st.date_input(label="Today")

        muscle_group = st.selectbox(label="Select Muscle Group", options=EXERCICES.keys())

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

                updated_df = pd.concat([gym, register_data], ignore_index=True)

                database.conn.update(worksheet="GYM", data=updated_df)

                st.success("Fitness Registed with Success!")


with tab3:
    muscle_group_train = st.selectbox(label="Select Muscle Group to Register Train", options=EXERCICES.keys())

    for key, item in DIVISION.items():
        if muscle_group_train in item:
            division_train = key
            break

    exercices = st.multiselect(label="Select all exercices of train", options=EXERCICES[muscle_group_train])

    if len(exercices) < 6:
        pad = 6 - len(exercices)
        exercices += ['*']*pad


    submit_btn = st.button("Register Train")

    if submit_btn:
            if not muscle_group_train:
                st.warning("Fill all fields")
                st.stop()

            else:
                exs = {i: exer for i, exer in enumerate(exercices)}
                register_train_dict = {
                    "Division Train": division_train,
                    "Muscle Group": muscle_group_train
                    } | exs

                register_data = pd.DataFrame([register_train_dict])

                updated_df = pd.concat([trains, register_data], ignore_index=True)

                database.conn.update(worksheet="TRAINS", data=updated_df)

                st.success("Train Registed with Success!")