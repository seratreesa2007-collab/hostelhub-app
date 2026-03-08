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
    st.header("Welcome to HostelHub")

    st.write(
        "HostelHub helps students find PG and hostel accommodations easily. "
        "Students can also submit complaints regarding maintenance."
    )

    st.subheader("Features")
    st.write("🔍 View available PGs and Hostels")
    st.write("📝 Submit complaints")
    st.write("⚡Simple and easy to use")


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