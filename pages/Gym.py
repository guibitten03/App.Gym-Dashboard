from library import *
from services.Database import Database

st.set_page_config(layout="wide")

st.title("📁 Crypto Trades Registed")
st.markdown("You can see all your trades bellow!")

database = Database(worksheets=[
    ("GYM", 6)
])

st.dataframe(database.worksheets["GYM"])