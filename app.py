import streamlit as st
import pandas as pd
import time

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="HostelHub", layout="wide")

# ------------------- UI STYLE -------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #f8f9fa, #e3f2fd);
}

/* Cards */
.card {
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}

/* Colors */
.home {background: #ffffff;}
.view {background: #e3f2fd;}
.add {background: #e8f5e9;}
.complaint {background: #fff3e0;}
.logs {background: #f3e5f5;}

/* Buttons */
div.stButton > button {
    background: linear-gradient(to right, #2a5298, #1e3c72);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

/* Titles */
h1, h2, h3 {
    color: #2a5298;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ------------------- LOADING -------------------
with st.spinner("Loading HostelHub..."):
    time.sleep(1)

# ------------------- FILE LOAD -------------------
def load_file(name, cols):
    try:
        return pd.read_csv(name)
    except:
        return pd.DataFrame(columns=cols)

hostels = load_file("hostels.csv", ["Name","Location","Rent","Contact"])
complaints = load_file("complaints.csv", ["Student","Hostel","Complaint"])
search_log = load_file("search_log.csv", ["Search"])
contact_log = load_file("contact_log.csv", ["Hostel","Student"])

# ------------------- TITLE -------------------
st.markdown("<h1>🏠 HostelHub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart PG & Hostel Finder</p>", unsafe_allow_html=True)

# ------------------- ROLE -------------------
role = st.sidebar.selectbox("Login As", ["Student", "Owner"])

# ------------------- OWNER PASSWORD -------------------
owner_access = False
if role == "Owner":
    password = st.sidebar.text_input("Enter Owner Password", type="password")

    if password == "owner123":
        owner_access = True
    else:
        st.sidebar.warning("Enter correct password")

# ------------------- MENU -------------------
menu = st.sidebar.selectbox("Menu",
    ["Home", "View Hostels"] +
    (["Submit Complaint"] if role=="Student" else []) +
    (["Add Hostel","View Complaints","View Searches","Contact Logs"] if owner_access else [])
)

# ------------------- LOCK -------------------
if role == "Owner" and not owner_access:
    st.warning("🔒 Owner section locked")

# ------------------- HOME -------------------
if menu == "Home":
    st.markdown("<div class='card home'>", unsafe_allow_html=True)

    st.markdown("## 🏠 Welcome to HostelHub")
    st.write("Find PGs and hostels easily, contact owners, and book rooms.")

    st.markdown("""
    ### 🌟 Features
    - 🔍 Search Hostels  
    - 📞 Contact Owners  
    - 📝 Submit Complaints  
    - ⚡ Fast & Simple  
    """)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- VIEW HOSTELS -------------------
elif menu == "View Hostels":
    st.markdown("<div class='card view'>", unsafe_allow_html=True)

    st.markdown("## 🔍 Available Hostels")

    search = st.text_input("Search")

    if search:
        filtered = hostels[
            hostels["Name"].str.contains(search, case=False) |
            hostels["Location"].str.contains(search, case=False)
        ]
        st.dataframe(filtered)
        pd.DataFrame({"Search":[search]}).to_csv("search_log.csv", mode="a", header=False, index=False)
    else:
        st.dataframe(hostels)

    if not hostels.empty:
        selected = st.selectbox("Select Hostel", hostels["Name"])

        if st.button("📞 Contact Owner & Book"):
            pd.DataFrame({
                "Hostel":[selected],
                "Student":["Student"]
            }).to_csv("contact_log.csv", mode="a", header=False, index=False)

            st.info(f"📩 Owner notified for {selected}")
            st.success("✅ Booking Successful!")
            st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- ADD HOSTEL -------------------
elif menu == "Add Hostel":
    st.markdown("<div class='card add'>", unsafe_allow_html=True)

    st.markdown("## ➕ Add Hostel")

    name = st.text_input("Name")
    location = st.text_input("Location")
    rent = st.text_input("Rent")
    contact = st.text_input("Contact")

    if st.button("Add"):
        pd.DataFrame({
            "Name":[name],
            "Location":[location],
            "Rent":[rent],
            "Contact":[contact]
        }).to_csv("hostels.csv", mode="a", header=False, index=False)

        st.success("🎉 Hostel Added!")
        st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- COMPLAINT -------------------
elif menu == "Submit Complaint":
    st.markdown("<div class='card complaint'>", unsafe_allow_html=True)

    st.markdown("## 📝 Submit Complaint")

    student = st.text_input("Name")
    hostel = st.text_input("Hostel")
    complaint = st.text_area("Complaint")

    if st.button("Submit"):
        pd.DataFrame({
            "Student":[student],
            "Hostel":[hostel],
            "Complaint":[complaint]
        }).to_csv("complaints.csv", mode="a", header=False, index=False)

        st.success("Complaint Submitted!")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- OWNER DATA -------------------
elif menu == "View Complaints":
    st.markdown("<div class='card logs'>", unsafe_allow_html=True)
    st.markdown("## Complaints")
    st.dataframe(load_file("complaints.csv", []))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "View Searches":
    st.markdown("<div class='card logs'>", unsafe_allow_html=True)
    st.markdown("## Searches")
    st.dataframe(load_file("search_log.csv", []))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Contact Logs":
    st.markdown("<div class='card logs'>", unsafe_allow_html=True)
    st.markdown("## Contact Logs")
    st.dataframe(load_file("contact_log.csv", []))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("""
<hr>
<p style='text-align:center;'>Made with ❤️ by HostelHub</p>
""", unsafe_allow_html=True)
