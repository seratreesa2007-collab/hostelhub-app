import streamlit as st
import pandas as pd

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="HostelHub", layout="wide")

# ------------------- LIGHT THEME -------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f8f9fa, #e3f2fd);
}
h1, h2, h3 {
    color: #2a5298;
}
</style>
""", unsafe_allow_html=True)

# ------------------- LOAD FILE FUNCTION -------------------
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
st.markdown("<h1 style='text-align:center;'>🏠 HostelHub</h1>", unsafe_allow_html=True)

# ------------------- ROLE -------------------
role = st.sidebar.selectbox("Login As", ["Student", "Owner"])

# ------------------- OWNER PASSWORD -------------------
owner_access = False

if role == "Owner":
    password = st.sidebar.text_input("Enter Owner Password", type="password")

    if password == "owner123":
        owner_access = True
    else:
        st.sidebar.warning("Enter correct password to access owner features")

# ------------------- MENU -------------------
menu = st.sidebar.selectbox("Menu",
    ["Home", "View Hostels"] +
    (["Submit Complaint"] if role=="Student" else []) +
    (["Add Hostel","View Complaints","View Searches","Contact Logs"] if owner_access else [])
)

# ------------------- LOCK MESSAGE -------------------
if role == "Owner" and not owner_access:
    st.warning("🔒 Owner section is locked. Please enter password.")

# ------------------- HOME -------------------
if menu == "Home":
    st.markdown("""
    <div style='background:white;padding:20px;border-radius:10px;text-align:center;'>
    <h2>Welcome to HostelHub</h2>
    <p>Find PGs and hostels easily. Contact owners and book rooms quickly.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------- VIEW HOSTELS -------------------
elif menu == "View Hostels":
    st.subheader("Available Hostels")

    search = st.text_input("🔍 Search by name/location")

    if search:
        filtered = hostels[
            hostels["Name"].str.contains(search, case=False) |
            hostels["Location"].str.contains(search, case=False)
        ]
        st.dataframe(filtered)

        pd.DataFrame({"Search":[search]}).to_csv("search_log.csv", mode="a", header=False, index=False)

    else:
        st.dataframe(hostels)

    # -------- CONTACT + BOOKING --------
    if not hostels.empty:
        selected = st.selectbox("Select Hostel", hostels["Name"])

        if st.button("📞 Contact Owner & Book Room"):

            # Save contact log
            pd.DataFrame({
                "Hostel":[selected],
                "Student":["Student"]
            }).to_csv("contact_log.csv", mode="a", header=False, index=False)

            # Owner message
            st.info(f"📩 Message sent to Owner: 'A student contacted you via HostelHub for {selected}'")

            # Student message
            st.success("✅ Booking Successful! Owner will contact you soon.")

# ------------------- ADD HOSTEL -------------------
elif menu == "Add Hostel":
    st.subheader("Add Hostel")

    name = st.text_input("Name")
    location = st.text_input("Location")
    rent = st.text_input("Rent")
    contact = st.text_input("Contact Number")

    if st.button("Add"):
        pd.DataFrame({
            "Name":[name],
            "Location":[location],
            "Rent":[rent],
            "Contact":[contact]
        }).to_csv("hostels.csv", mode="a", header=False, index=False)

        st.success("Hostel Added!")

# ------------------- SUBMIT COMPLAINT -------------------
elif menu == "Submit Complaint":
    st.subheader("Submit Complaint")

    student = st.text_input("Your Name")
    hostel = st.text_input("Hostel Name")
    complaint = st.text_area("Complaint")

    if st.button("Submit"):
        pd.DataFrame({
            "Student":[student],
            "Hostel":[hostel],
            "Complaint":[complaint]
        }).to_csv("complaints.csv", mode="a", header=False, index=False)

        st.success("Complaint Submitted!")

# ------------------- VIEW COMPLAINTS -------------------
elif menu == "View Complaints":
    st.subheader("Complaints")
    st.dataframe(load_file("complaints.csv", []))

# ------------------- VIEW SEARCHES -------------------
elif menu == "View Searches":
    st.subheader("Search Logs")
    st.dataframe(load_file("search_log.csv", []))

# ------------------- CONTACT LOG -------------------
elif menu == "Contact Logs":
    st.subheader("Contact Logs (For Commission)")
    st.dataframe(load_file("contact_log.csv", []))
