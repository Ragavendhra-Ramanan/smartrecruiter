# streamlit_app.py
import streamlit as st

def main():
    st.title("User Input Form")

    # Get user inputs
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=0, max_value=150, value=25)
    email = st.text_input("Enter your email address:")

    # Display user inputs
    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Email: {email}")

if __name__ == "__main__":
    main()
