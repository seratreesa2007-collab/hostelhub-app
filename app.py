import streamlit as st
import pandas as pd
import os

st.title("🏠 HostelHub - Smart PG & Hostel Finder")

# Role selection
role = st.sidebar.selectbox("Login As", ["Student", "Owner"])

# Menu based on role
if role == "Student":
    menu = st.sidebar.selectbox("Menu", ["Home", "View PG/Hostels", "Submit Complaint"])
else:
    menu = st.sidebar.selectbox("Menu", ["Home", "Add PG/Hostel", "View Complaints", "View Searches"])

# Create files if they don't exist
if not os.path.exists("hostels.csv"):
    df = pd.DataFrame(columns=["Name","Location","Rent","Facilities","Contact"])
    df.to_csv("hostels.csv", index=False)

if not os.path.exists("complaints.csv"):
    df = pd.DataFrame(columns=["Name","Hostel","Complaint"])
    df.to_csv("complaints.csv", index=False)


# HOME PAGE
if menu == "Home":

    # Background + Text Color
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🏠 HostelHub</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Smart PG & Hostel Finder</h3>", unsafe_allow_html=True)

    st.write("")

    # Welcome Box
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
    <h3>Welcome to HostelHub</h3>
    <p>This platform helps students find PG and hostel accommodation easily. 
    You can also submit complaints regarding maintenance issues.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Features Section
    st.markdown("### 🌟 Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - 🔍 View available PGs and Hostels  
        - 📍 Search by location  
        """)

    with col2:
        st.markdown("""
        - 📝 Submit complaints  
        - ⚡ Simple and easy to use  
        """)

    st.write("")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Made with ❤️ for students</p>", unsafe_allow_html=True)

   
    

# VIEW HOSTELS
elif menu == "View PG/Hostels":
    st.header("Available PG/Hostels")

    search = st.text_input("Search Hostel or Location")

    data = pd.read_csv("hostels.csv")

    if search:
        filtered = data[
            data["Name"].str.contains(search, case=False) |
            data["Location"].str.contains(search, case=False)
        ]

        st.dataframe(filtered)

        # Save search
        log = pd.DataFrame({"Search":[search]})
        log.to_csv("search_log.csv", mode="a", header=False, index=False)

    else:
        st.dataframe(data)


# ADD HOSTEL
elif menu == "Add PG/Hostel":
    st.header("Add PG/Hostel")

    name = st.text_input("Hostel Name")
    location = st.text_input("Location")
    rent = st.number_input("Rent")
    facilities = st.text_input("Facilities")
    contact = st.text_input("Contact Number")

    if st.button("Add Hostel"):

        new_data = pd.DataFrame({
            "Name":[name],
            "Location":[location],
            "Rent":[rent],
            "Facilities":[facilities],
            "Contact":[contact]
        })

        new_data.to_csv("hostels.csv", mode="a", header=False, index=False)

        st.success("Hostel Added Successfully!")


# SUBMIT COMPLAINT
elif menu == "Submit Complaint":
    st.header("Submit Complaint")

    student_name = st.text_input("Your Name")
    hostel_name = st.text_input("Hostel Name")
    complaint = st.text_area("Complaint")

    if st.button("Submit Complaint"):

        new_complaint = pd.DataFrame({
            "Name":[student_name],
            "Hostel":[hostel_name],
            "Complaint":[complaint]
        })

        new_complaint.to_csv("complaints.csv", mode="a", header=False, index=False)

        st.success("Complaint Submitted Successfully!")


# VIEW COMPLAINTS
elif menu == "View Complaints":
    st.header("Complaints")

    data = pd.read_csv("complaints.csv")

    if data.empty:
        st.warning("No complaints submitted yet.")
    else:
        st.dataframe(data)
elif menu == "View Searches":
    st.header("Student Search History")

    data = pd.read_csv("search_log.csv")

    if data.empty:
        st.warning("No searches yet")
    else:
        st.dataframe(data)
