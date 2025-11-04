import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Restaurant Booking", layout="wide")
st.title("Restaurant Reservation Booking System")


restaurants = {
    "Amirtha Fine Dining": "amirtha.png",
    "Zaitoon": "zaitoon.png",
    "The Vellore Kitchen": "vellore kitchen.png",
    "Signature": "signature.png"
}


if "reservations" not in st.session_state:
    st.session_state.reservations = []

if "selected_restaurant" not in st.session_state:
    st.session_state.selected_restaurant = None



def is_valid_time(time_str):
    """Check if time is in proper HH:MM 24-hour format"""
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    return re.match(pattern, time_str) is not None


def is_valid_email(email):
    """Check if email format is valid"""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None



def add_reservation(restaurant, name, people, date, time, email):
    """Add a new reservation"""
    st.session_state.reservations.append({
        "Restaurant": restaurant,
        "Name": name,
        "People": people,
        "Date": date,
        "Time": time,
        "Email": email
    })
    st.success(f"Reservation added for {name} at {restaurant} on {date} at {time}")
    st.session_state.selected_restaurant = None


def view_reservations():
    """View all reservations"""
    if len(st.session_state.reservations) == 0:
        st.info("No reservations found yet.")
    else:
        df = pd.DataFrame(st.session_state.reservations)
        st.dataframe(df)


def cancel_reservation(email):
    """Cancel reservation using email"""
    found = False
    for r in st.session_state.reservations:
        if r["Email"].lower() == email.lower():
            st.session_state.reservations.remove(r)
            found = True
            st.warning(f" Reservation under {email} has been cancelled.")
            break
    if not found:
        st.error("No reservation found for that email.")



menu = ["Home", "View Reservations", "Cancel Reservation"]
choice = st.sidebar.selectbox("Menu", menu)


if choice == "Home" and not st.session_state.selected_restaurant:
    st.header("Choose a Restaurant to Reserve")

    cols = st.columns(4)
    for i, (name, img_url) in enumerate(restaurants.items()):
        with cols[i]:
            st.image(img_url, caption=name, use_container_width=True)
            if st.button(f"Reserve at {name}", key=name):
                st.session_state.selected_restaurant = name
                st.rerun()


if st.session_state.selected_restaurant:
    st.header(f" Make a Reservation at {st.session_state.selected_restaurant}")

    name = st.text_input("Customer Name")
    people = st.number_input("Number of People", min_value=1, max_value=20)
    date = st.date_input("Reservation Date")
    time = st.text_input("Time (HH:MM) — 24-hour format, e.g. 18:30")
    email = st.text_input("Email Address")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm Reservation"):
            # Field validation
            if not name or not time or not email:
                st.error("Please fill all fields!")
            elif not is_valid_time(time):
                st.error("Please enter a valid time in HH:MM format (24-hour clock). Example: 19:45")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address. Example: example@gmail.com")
            else:
                add_reservation(st.session_state.selected_restaurant, name, people, str(date), time, email)

    with col2:
        if st.button("Go Back"):
            st.session_state.selected_restaurant = None
            st.rerun()



elif choice == "View Reservations":
    st.header("All Reservations")
    view_reservations()


elif choice == "Cancel Reservation":
    st.header("Cancel a Reservation")
    email = st.text_input("Enter your Email Address to cancel reservation:")
    if st.button("Cancel Reservation"):
        if not email:
            st.error("Please enter an email!")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address format.")
        else:
            cancel_reservation(email)


st.set_page_config(page_title="My App", layout="wide")


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




