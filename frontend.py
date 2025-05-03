# ==========================
# frontend.py (Streamlit)
# ==========================
import streamlit as st
import requests

#API_URL = "http://127.0.0.1:8000"
API_URL = "https://oboe-reed-production.up.railway.app"


st.title("🎵 Oboe Reed Logger")

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
scrape = st.text_input('Scrape')
notes = st.text_area("Other notes")

if st.button("Save Reed"):
    r = requests.post(
        f"{API_URL}/reeds/",
        json={
            "name": name,
            "instrument": instrument,
            "cane_type": cane_type,
            "shape": shape,
            "staple": staple,
            "gouge": gouge,
            "scrape": scrape,
            "notes": notes
        },
    )
    if r.status_code == 200:
        st.success("Reed saved")
    else:
        st.error("Failed to save reed")



st.header("Existing Reeds")
reeds = requests.get(f"{API_URL}/reeds/").json()

for reed in reeds:
    with st.expander(reed['name']):
        st.write(f"Created: {reed['created_at']}")
        st.write(f"Instrument: {reed.get('instrument', '')}")
        st.write(f"Cane type: {reed.get('cane_type', '')}")
        st.write(f"Shape: {reed.get('shape', '')}")
        st.write(f"Staple: {reed.get('staple', '')}")
        st.write(f"Gouge: {reed.get('gouge', '')}")
        st.write(f"Scrape: {reed.get('scrape', '')}")
        st.text(f"Notes:\n{reed['notes']}")

        new_note = st.text_area(f"Add note to {reed['name']}", key=f"note_{reed['id']}")
        if st.button("Add Note", key=f"btn_{reed['id']}"):
            res = requests.post(
                f"{API_URL}/reeds/{reed['id']}/add_note",
                json={"notes": new_note}
            )
            if res.status_code == 200:
                st.success("Note added")
        
        if st.button("Delete Reed", key=f"delete_{reed['id']}"):
            confirm = st.warning(f"Are you sure you want to delete {reed['name']}?")
            if st.button("Confirm Delete", key=f"confirm_delete_{reed['id']}"):
                res = requests.delete(f"{API_URL}/reeds/{reed['id']}/")
                if res.status_code == 200:
                    st.success("Reed deleted — refresh to update")
                else:
                    st.error("Failed to delete reed")


