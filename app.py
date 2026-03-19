import streamlit as st
import pandas as pd

# ------------------- FILE SETUP -------------------
try:
    hostels = pd.read_csv("hostels.csv")
except:
    hostels = pd.DataFrame(columns=["Name", "Location", "Rent", "Contact"])

try:
    complaints = pd.read_csv("complaints.csv")
except:
    complaints = pd.DataFrame(columns=["Student", "Hostel", "Complaint"])

try:
    search_log = pd.read_csv("search_log.csv")
except:
    search_log = pd.DataFrame(columns=["Search"])

try:
    contact_log = pd.read_csv("contact_log.csv")
except:
    contact_log = pd.DataFrame(columns=["Hostel", "Contacted_By"])

# ------------------- TITLE -------------------
st.title("🏠 HostelHub")

# ------------------- LOGIN TYPE -------------------
role = st.sidebar.selectbox("Login As", ["Student", "Owner"])

menu = st.sidebar.selectbox("Menu",
    ["Home", "View PG/Hostels"] +
    (["Submit Complaint"] if role == "Student" else []) +
    (["Add Hostel", "View Complaints", "View Searches", "Contact Logs"] if role == "Owner" else [])
)

# ------------------- HOME -------------------
if menu == "Home":
    st.subheader("Welcome to HostelHub")
    st.write("Find PGs and hostels easily.")

# ------------------- VIEW HOSTELS -------------------
elif menu == "View PG/Hostels":
    st.subheader("Available Hostels")

    search = st.text_input("Search by name or location")

    if search:
        filtered = hostels[
            hostels["Name"].str.contains(search, case=False) |
            hostels["Location"].str.contains(search, case=False)
        ]
        st.dataframe(filtered)

        # Save search
        pd.DataFrame({"Search": [search]}).to_csv("search_log.csv", mode="a", header=False, index=False)

    else:
        st.dataframe(hostels)

    # Contact owner (important for commission idea)
    if not hostels.empty:
        hostel_name = st.selectbox("Select Hostel to Contact", hostels["Name"])

        if st.button("📞 Contact Owner"):
            pd.DataFrame({
                "Hostel": [hostel_name],
                "Contacted_By": ["Student"]
            }).to_csv("contact_log.csv", mode="a", header=False, index=False)

            st.success("Owner contacted! (Tracked)")

# ------------------- ADD HOSTEL (OWNER) -------------------
elif menu == "Add Hostel":
    st.subheader("Add Hostel")

    name = st.text_input("Hostel Name")
    location = st.text_input("Location")
    rent = st.text_input("Rent")
    contact = st.text_input("Contact")

    if st.button("Add Hostel"):
        new_data = pd.DataFrame({
            "Name": [name],
            "Location": [location],
            "Rent": [rent],
            "Contact": [contact]
        })

        new_data.to_csv("hostels.csv", mode="a", header=False, index=False)
        st.success("Hostel added successfully!")

# ------------------- SUBMIT COMPLAINT (STUDENT) -------------------
elif menu == "Submit Complaint":
    st.subheader("Submit Complaint")

    student = st.text_input("Your Name")
    hostel = st.text_input("Hostel Name")
    complaint = st.text_area("Complaint")

    if st.button("Submit"):
        new_data = pd.DataFrame({
            "Student": [student],
            "Hostel": [hostel],
            "Complaint": [complaint]
        })

        new_data.to_csv("complaints.csv", mode="a", header=False, index=False)
        st.success("Complaint submitted!")

# ------------------- VIEW COMPLAINTS (OWNER) -------------------
elif menu == "View Complaints":
    st.subheader("All Complaints")

    try:
        data = pd.read_csv("complaints.csv")
        st.dataframe(data)
    except:
        st.warning("No complaints yet")

# ------------------- VIEW SEARCHES -------------------
elif menu == "View Searches":
    st.subheader("Search History")

    try:
        data = pd.read_csv("search_log.csv")
        st.dataframe(data)
    except:
        st.warning("No searches yet")

# ------------------- CONTACT LOG (IMPORTANT) -------------------
elif menu == "Contact Logs":
    st.subheader("Student Contact Logs")

    try:
        data = pd.read_csv("contact_log.csv")
        st.dataframe(data)
    except:
        st.warning("No contacts yet")
