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

        instrument = st.text_input("Instrument", reed.get('instrument', ''), key=f"instrument_{reed['id']}")
        cane_type = st.text_input("Cane Type", reed.get('cane_type', ''), key=f"cane_{reed['id']}")
        shape = st.text_input("Shape", reed.get('shape', ''), key=f"shape_{reed['id']}")
        staple = st.text_input("Staple", reed.get('staple', ''), key=f"staple_{reed['id']}")
        gouge = st.text_input("Gouge", reed.get('gouge', ''), key=f"gouge_{reed['id']}")
        scrape = st.text_input("Scrape", reed.get('scrape', ''), key=f"scrape_{reed['id']}")
        notes = st.text_area("Notes (editable)", reed.get('notes', ''), key=f"notes_{reed['id']}")

        if st.button("Save Changes", key=f"btn_save_{reed['id']}"):
            update_data = {
                "instrument": instrument,
                "cane_type": cane_type,
                "shape": shape,
                "staple": staple,
                "gouge": gouge,
                "scrape": scrape,
                "notes": notes  # updated notes!
            }
            res = requests.put(f"{API_URL}/reeds/{reed['id']}/", json=update_data)
            if res.status_code == 200:
                st.success("Reed updated")
            else:
                st.error("Update failed")

        if st.button("Delete Reed", key=f"delete_{reed['id']}"):
            res = requests.delete(f"{API_URL}/reeds/{reed['id']}/")
            if res.status_code == 200:
                st.success("Reed deleted — refresh to update")
                st.rerun()
            else:
                st.error("Failed to delete reed")
