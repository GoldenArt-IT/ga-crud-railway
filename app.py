import streamlit as st
from sqlalchemy import create_engine, text
import os

# Connect to DB
db_url = os.getenv("db_url")
engine = create_engine(db_url)

# CRUD Functions
def get_users():
    with engine.connect() as conn:
        return conn.execute(text("SELECT * FROM users")).fetchall()

def add_user(name, email, role):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users (name, email, role) VALUES (:n, :e, :r)"),
                     {"n": name, "e": email, "r": role})

def update_user(id, name, email, role):
    with engine.begin() as conn:
        conn.execute(text("UPDATE users SET name=:n, email=:e, role=:r WHERE id=:i"),
                     {"i": id, "n": name, "e": email, "r": role})

def delete_user(id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM users WHERE id=:i"), {"i": id})

# Streamlit UI
st.title("User Management")

menu = st.sidebar.selectbox("Action", ["View", "Add", "Update", "Delete"])

if menu == "View":
    users = get_users()
    st.write(users)

elif menu == "Add":
    name = st.text_input("Name")
    email = st.text_input("Email")
    role = st.text_input("Role")
    if st.button("Add"):
        add_user(name, email, role)
        st.success("User added.")

elif menu == "Update":
    id = st.number_input("User ID", step=1)
    name = st.text_input("New Name")
    email = st.text_input("New Email")
    role = st.text_input("New Role")
    if st.button("Update"):
        update_user(id, name, email, role)
        st.success("User updated.")

elif menu == "Delete":
    id = st.number_input("User ID to delete", step=1)
    if st.button("Delete"):
        delete_user(id)
        st.success("User deleted.")
