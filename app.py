from library import *
from services.Database import Database


database = Database(worksheets=[
    ("GYM", 9)
])

st.dataframe(database.worksheets['GYM'])