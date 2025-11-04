import streamlit as st
from datetime import datetime

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="Restaurant Reservation", layout="wide")
st.title("Restaurant Reservation System")

# -------------------------------
# RESTAURANT DATA
# -------------------------------
restaurants = {
    "Amirtha Fine Dining": "amirtha.png",
    "Zaitoon": "zaitoon.png",
    "The Vellore Kitchen": "vellore kitchen.png",
    "Signature": "signature.png"
}

# Store reservations
if "reservations" not in st.session_state:
    st.session_state.reservations = []

# Store selected restaurant
if "selected_restaurant" not in st.session_state:
    st.session_state.selected_restaurant = None


# -------------------------------
# SIMPLE VALIDATION FUNCTIONS
# -------------------------------
def check_time_format(time):
    """Check if time is in HH:MM format"""
    try:
        datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False


def check_email_format(email):
    """Check if email has '@' and '.'"""
    return "@" in email and "." in email


# -------------------------------
# MAIN FUNCTIONS
# -------------------------------
def add_reservation(restaurant, name, people, date, time, email):
    """Add a reservation"""
    reservation = {
        "Restaurant": restaurant,
        "Name": name,
        "People": people,
        "Date": date,
        "Time": time,
        "Email": email
    }
    st.session_state.reservations.append(reservation)
    st.success(f"Reservation added for {name} at {restaurant} on {date} at {time}!")


def view_reservations():
    """Display all reservations"""
    if not st.session_state.reservations:
        st.info("No reservations yet.")
    else:
        st.write("### All Reservations:")
        for r in st.session_state.reservations:
            st.write(f" {r['Restaurant']} |  {r['Name']} |  {r['People']} |  {r['Date']} |  {r['Time']} | 📧 {r['Email']}")


def cancel_reservation(email):
    """Cancel reservation using email"""
    for r in st.session_state.reservations:
        if r["Email"].lower() == email.lower():
            st.session_state.reservations.remove(r)
            st.warning(f"Reservation under {email} has been cancelled.")
            return
    st.error("No reservation found for that email.")


# -------------------------------
# SIDEBAR MENU
# -------------------------------
menu = ["Home", "View Reservations", "Cancel Reservation"]
choice = st.sidebar.selectbox("Menu", menu)


# -------------------------------
# HOME PAGE (CLICKABLE IMAGES)
# -------------------------------
if choice == "Home" and not st.session_state.selected_restaurant:
    st.header("Choose a Restaurant to Make a Reservation")

    cols = st.columns(4)
    for i, (name, img) in enumerate(restaurants.items()):
        with cols[i]:
            st.image(img, caption=name, use_container_width=True)
            if st.button(f"Reserve at {name}", key=name):
                st.session_state.selected_restaurant = name
                st.rerun()


# -------------------------------
# RESERVATION FORM
# -------------------------------
if st.session_state.selected_restaurant:
    st.header(f"Reserve a Table at {st.session_state.selected_restaurant}")

    name = st.text_input("Your Name")
    people = st.number_input("Number of People", min_value=1, max_value=20)
    date = st.date_input("Reservation Date")
    time = st.text_input("Time (HH:MM - 24-hour format)")
    email = st.text_input("Email Address")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm Reservation"):
            if not name or not time or not email:
                st.error("Please fill all fields.")
            elif not check_time_format(time):
                st.error("Enter a valid time in HH:MM format.")
            elif not check_email_format(email):
                st.error("Enter a valid email (example: name@gmail.com).")
            else:
                add_reservation(st.session_state.selected_restaurant, name, people, str(date), time, email)
                st.session_state.selected_restaurant = None

    with col2:
        if st.button("Go Back"):
            st.session_state.selected_restaurant = None
            st.rerun()


# -------------------------------
# VIEW RESERVATIONS
# -------------------------------
elif choice == "View Reservations":
    st.header("📋 All Reservations")
    view_reservations()


# -------------------------------
# CANCEL RESERVATION
# -------------------------------
elif choice == "Cancel Reservation":
    st.header("Cancel Reservation")
    email = st.text_input("Enter your Email Address")
    if st.button("Cancel Reservation"):
        if not email:
            st.error("Please enter your email.")
        elif not check_email_format(email):
            st.error("Invalid email format.")
        else:
            cancel_reservation(email)


import base64

def set_bg(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

set_bg("bgpic.png")




