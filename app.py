import streamlit as st
import pandas as pd
import os

st.title("🏠 HostelHub - Smart PG & Hostel Finder")

# Role selection
role = st.selectbox("Login As", ["Student", "Owner"])
role = st.sidebar.selectbox("Login As", ["Student", "Owner"])

# Menu based on role
if role == "Student":
    menu = st.sidebar.selectbox("Menu", ["Home", "View PG/Hostels", "Submit Complaint"])
else:
    menu = st.sidebar.selectbox("Menu", ["Home", "Add PG/Hostel", "View Complaints", "View Contacts"])

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
      elif menu == "View Contacts":
    st.header("Student Contacts")

    owner_name = st.text_input("Enter your name")

    data = pd.read_csv("contact_log.csv", names=["Hostel","Owner"])

    filtered = data[data["Owner"] == owner_name]

    st.dataframe(filtered)
    st.header("Available Hostels")

    data = pd.read_csv("hostels.csv")

    for i, row in data.iterrows():
        st.write(f"🏠 {row['Name']} - {row['Location']} - ₹{row['Rent']}")

        if st.button(f"Contact Owner {i}"):
            log = pd.DataFrame({
                "Hostel":[row["Name"]],
                "Owner":[row["Owner"]]
            })
            log.to_csv("contact_log.csv", mode="a", header=False, index=False)

            st.success("Owner contact recorded") 
  

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

    student = st.text_input("Student Name")
    hostel = st.text_input("Hostel Name")
    owner = st.text_input("Owner Name")  # NEW
    complaint = st.text_area("Complaint")

    if st.button("Submit"):
        data = pd.DataFrame({
            "Student":[student],
            "Hostel":[hostel],
            "Owner":[owner],
            "Complaint":[complaint]
        })
        data.to_csv("complaints.csv", mode="a", header=False, index=False)
        st.success("Complaint submitted")


# VIEW COMPLAINTS
elif menu == "View Complaints":
    st.header("Complaints")

    owner_name = st.text_input("Enter your name")

    data = pd.read_csv("complaints.csv", names=["Student","Hostel","Owner","Complaint"])

    filtered = data[data["Owner"] == owner_name]

    st.dataframe(filtered)
elif menu == "View Searches":
    st.header("Student Search History")

    data = pd.read_csv("search_log.csv")

    if data.empty:
        st.warning("No searches yet")
    else:
        st.dataframe(data)
        
