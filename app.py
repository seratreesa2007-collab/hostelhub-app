import streamlit as st
import pandas as pd

st.set_page_config(page_title="HostelHub", layout="centered")

# 🎨 LIGHT THEME
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f8ffae, #43c6ac);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- ROLE ----------------
role = st.selectbox("Login As", ["Student", "Owner"])

# ---------------- MENU ----------------
if role == "Student":
    menu = st.sidebar.selectbox("Menu", ["Home", "View Hostels", "Submit Complaint"])
else:
    menu = st.sidebar.selectbox("Menu", ["Home", "Add Hostel", "View Complaints", "View Contacts"])


# ---------------- HOME ----------------
if menu == "Home":

    st.markdown("<h1 style='text-align:center;'>🏠 HostelHub</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Smart PG & Hostel Finder</h4>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color:white; padding:20px; border-radius:10px;'>
    <h3>Welcome</h3>
    <p>This platform helps students find hostels and connect with owners easily.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("### 🌟 Features")
    st.write("✔ View hostels")
    st.write("✔ Submit complaints (only visible to owner)")
    st.write("✔ Contact owner tracking (for commission)")

    st.write("")

    # 🧠 EXPLANATION BOX (YOUR DOUBT SOLUTION)
    st.markdown("""
    <div style='background-color:#ffffff; padding:15px; border-radius:10px;'>
    <h4>System Improvements</h4>
    <ul>
    <li>Role-based access (Student / Owner)</li>
    <li>Complaints are visible only to respective owners</li>
    <li>Contact tracking helps identify student-owner interaction</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


# ---------------- ADD HOSTEL ----------------
elif menu == "Add Hostel":
    st.header("Add Hostel")

    name = st.text_input("Hostel Name")
    location = st.text_input("Location")
    rent = st.text_input("Rent")
    owner = st.text_input("Owner Name")

    if st.button("Add Hostel"):
        data = pd.DataFrame({
            "Name":[name],
            "Location":[location],
            "Rent":[rent],
            "Owner":[owner]
        })
        data.to_csv("hostels.csv", mode="a", header=False, index=False)
        st.success("Hostel Added Successfully")


# ---------------- VIEW HOSTELS ----------------
elif menu == "View Hostels":
    st.header("Available Hostels")

    try:
        data = pd.read_csv("hostels.csv", names=["Name","Location","Rent","Owner"])

        for i, row in data.iterrows():
            st.markdown(f"""
            <div style='background-color:white; padding:10px; border-radius:10px; margin-bottom:10px;'>
            <b>{row['Name']}</b><br>
            📍 {row['Location']}<br>
            💰 ₹{row['Rent']}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Contact Owner {i}"):
                log = pd.DataFrame({
                    "Hostel":[row["Name"]],
                    "Owner":[row["Owner"]]
                })
                log.to_csv("contact_log.csv", mode="a", header=False, index=False)

                st.success("Owner contact recorded (used for commission)")

    except:
        st.warning("No hostels available")


# ---------------- SUBMIT COMPLAINT ----------------
elif menu == "Submit Complaint":
    st.header("Submit Complaint")

    student = st.text_input("Student Name")
    hostel = st.text_input("Hostel Name")
    owner = st.text_input("Owner Name")
    complaint = st.text_area("Complaint")

    if st.button("Submit"):
        data = pd.DataFrame({
            "Student":[student],
            "Hostel":[hostel],
            "Owner":[owner],
            "Complaint":[complaint]
        })
        data.to_csv("complaints.csv", mode="a", header=False, index=False)
        st.success("Complaint submitted successfully")


# ---------------- VIEW COMPLAINTS ----------------
elif menu == "View Complaints":
    st.header("View Complaints")

    owner_name = st.text_input("Enter your name")

    try:
        data = pd.read_csv("complaints.csv", names=["Student","Hostel","Owner","Complaint"])
        filtered = data[data["Owner"] == owner_name]

        st.dataframe(filtered)

    except:
        st.warning("No complaints found")


# ---------------- VIEW CONTACTS ----------------
elif menu == "View Contacts":
    st.header("Student Contacts")

    owner_name = st.text_input("Enter your name")

    try:
        data = pd.read_csv("contact_log.csv", names=["Hostel","Owner"])
        filtered = data[data["Owner"] == owner_name]

        st.dataframe(filtered)

    except:
        st.warning("No contact data available")
