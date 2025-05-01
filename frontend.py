# ==========================
# frontend.py (Streamlit)
# ==========================
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("🎵 Oboe Reed Logger")

st.header("Add a New Reed")
name = st.text_input("Reed name")
notes = st.text_area("Initial notes")
if st.button("Save Reed"):
    r = requests.post(f"{API_URL}/reeds/", json={"name": name, "notes": notes})
    if r.status_code == 200:
        st.success("Reed saved")

st.header("Existing Reeds")
reeds = requests.get(f"{API_URL}/reeds/").json()
for reed in reeds:
    with st.expander(reed['name']):
        st.write(f"Created: {reed['created_at']}")
        st.text(reed['notes'])
        new_note = st.text_area(f"Add note to {reed['name']}", key=f"note_{reed['id']}")
        if st.button("Add Note", key=f"btn_{reed['id']}"):
            res = requests.post(f"{API_URL}/reeds/{reed['id']}/add_note", json={"notes": new_note})
            if res.status_code == 200:
                st.success("Note added")