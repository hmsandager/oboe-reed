# ==========================
# frontend.py (Streamlit)
# ==========================
import streamlit as st
import requests
import datetime
from collections import defaultdict

#API_URL = "http://127.0.0.1:8000"
API_URL = "https://oboe-reed-production.up.railway.app"


st.title("🎵 Oboe Reed Logger")

st.sidebar.header("Login")

if "user_id" not in st.session_state:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        res = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state["user_id"] = res.json()["user_id"]
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Login failed")



st.header("Add a New Reed")
name = st.text_input("Reed number")
instrument = st.selectbox(
    "Instrument",
    ["Oboe", "English Horn", "Oboe d'Amore"]
)

cane_type = st.text_input("Cane type")
shape = st.text_input("Shape")
staple = st.text_input('Staple')
gouge = st.text_input('Gouge')
reed_length = st.text_input('Reed length')
density = st.text_input('Cane density')
scrape = st.text_area('Scrape')
notes = st.text_area("Other notes")
quality = st.text_area('Describe how the reed plays')

if st.button("Save Reed"):
    r = requests.post(
        f"{API_URL}/reeds/",
        json={
            "user_id": st.session_state.get("user_id"),
            "name": name,
            "instrument": instrument,
            "cane_type": cane_type,
            "shape": shape,
            "staple": staple,
            "gouge": gouge,
            'reed_length': reed_length,
            "density": density,
            "scrape": scrape,
            "notes": notes,
            "quality": quality
        },
    )
    if r.status_code == 200:
        st.success("Reed saved")
    else:
        st.error("Failed to save reed")





st.header("Existing Reeds")

# Step 1: Fetch all reeds
reeds = requests.get(f"{API_URL}/reeds/", params={"user_id": st.session_state.get("user_id")}).json()

# Step 2: Parse dates and group reeds by (year, month)
grouped_reeds = defaultdict(list)
years = set()
months = set()

for reed in reeds:
    created_date = datetime.datetime.fromisoformat(reed['created_at'])
    year = created_date.year
    month = created_date.month
    years.add(year)
    months.add(month)
    grouped_reeds[(year, month)].append(reed)

# Step 3: Create dropdowns
current_date = datetime.datetime.now()
selected_year = st.selectbox("Select Year", sorted(years, reverse=True), index=0)
selected_month = st.selectbox(
    "Select Month",
    sorted(months),
    index=sorted(months).index(current_date.month) if current_date.month in months else 0,
    format_func=lambda m: datetime.date(1900, m, 1).strftime('%B')  # show "January", etc.
)

# Step 4: Filter and display reeds
selected_reeds = sorted(
    grouped_reeds.get((selected_year, selected_month), []),
    key=lambda r: datetime.datetime.fromisoformat(r['created_at'])
)

st.subheader(f"Reeds created in {datetime.date(1900, selected_month, 1).strftime('%B')} {selected_year}")

if not selected_reeds:
    st.info("No reeds found for this month.")
else:
    for reed in selected_reeds:
        with st.expander(reed['name']):
            st.write(f"Created: {reed['created_at']}")

            instrument = st.selectbox(
                "Instrument",
                ["Oboe", "English Horn", "Oboe d'Amore"],
                index=["Oboe", "English Horn", "Oboe d'Amore"].index(reed.get('instrument', 'Oboe')),
                key=f"instrument_{reed['id']}"
            )
            cane_type = st.text_input("Cane Type", reed.get('cane_type', ''), key=f"cane_{reed['id']}")
            shape = st.text_input("Shape", reed.get('shape', ''), key=f"shape_{reed['id']}")
            staple = st.text_input("Staple", reed.get('staple', ''), key=f"staple_{reed['id']}")
            gouge = st.text_input("Gouge", reed.get('gouge', ''), key=f"gouge_{reed['id']}")
            reed_length = st.text_input('Reed length', reed.get('reed_length', ''), key=f"reed_length_{reed['id']}")
            density = st.text_input('Cane density', reed.get('density', ''), key=f"density_{reed['id']}")
            scrape = st.text_area("Scrape", reed.get('scrape', ''), key=f"scrape_{reed['id']}")
            notes = st.text_area("Notes", reed.get('notes', ''), key=f"notes_{reed['id']}")
            quality = st.text_area("Describe how the reed plays", reed.get('quality', ''), key=f"quality_{reed['id']}")
            

            if st.button("Save Changes", key=f"btn_save_{reed['id']}"):
                # When building the update_data dict
                update_data = {
                    "user_id": st.session_state.get("user_id"),
                    "instrument": instrument or "",
                    "cane_type": cane_type or "",
                    "shape": shape or "",
                    "staple": staple or "",
                    "gouge": gouge or "",
                    "reed_length": reed_length or "",
                    "density": density or "",
                    "scrape": scrape or "",
                    "notes": notes or "",
                    "quality": quality or ""
                }

                res = requests.put(f"{API_URL}/reeds/{reed['id']}/", json=update_data)
                if res.status_code == 200:
                    st.success("Reed updated")
                else:
                    st.error("Update failed")
                    st.text(f"Status: {res.status_code}")
                    st.text(f"Response: {res.text}")


            if st.button("Delete Reed", key=f"delete_{reed['id']}"):
                res = requests.delete(f"{API_URL}/reeds/{reed['id']}/")
                if res.status_code == 200:
                    st.success("Reed deleted — refresh to update")
                    st.rerun()
                else:
                    st.error("Failed to delete reed")
