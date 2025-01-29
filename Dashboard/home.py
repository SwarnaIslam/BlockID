import streamlit as st
import requests
import tenseal as ts
from cryptography.fernet import Fernet
import hashlib
import base64
import numpy as np
from PIL import Image

st.set_page_config(page_title="User Dashboard", layout="centered")

public_address = st.query_params["public_address"]
user_id = st.query_params["userId"]

if not public_address or not user_id:
    st.error("Missing parameters! Ensure public_address and userId are provided in the URL.")
    st.stop()

st.title("User Dashboard")
st.subheader(f"User ID: {user_id}")

password = st.text_input("Enter your password:", type="password")
decrypt_button = st.button("Retrieve Data")

def fetch_from_ipfs(cid):
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def decrypt_fhe_private_key(encrypted_key: bytes, password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    fernet = Fernet(fernet_key)
    
    try:
        return fernet.decrypt(encrypted_key)
    except:
        st.error("Incorrect password! Unable to decrypt the private key.")
        return None

if decrypt_button:
    with st.status("Retrieving and decrypting data... Please wait."):
        user_metadata = fetch_from_ipfs(user_id)
        
        if not user_metadata:
            st.stop()
        
        public_key_cid = user_metadata["fhe_public_key"]
        private_key_cid = user_metadata["fhe_private_key"]
        image_cid = user_metadata["encrypted_image"]

        encrypted_private_key = requests.get(f"https://gateway.pinata.cloud/ipfs/{private_key_cid}", stream=True).content
        encrypted_image_data = requests.get(f"https://gateway.pinata.cloud/ipfs/{image_cid}", stream=True).content

        decrypted_private_key = decrypt_fhe_private_key(encrypted_private_key, password)
        if not decrypted_private_key:
            st.stop()

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("### User Information:")
            st.write(f"**Name:** {user_metadata['name']}")
            st.write(f"**DOB:** {user_metadata['dob']}")
            st.write(f"**address:** {user_metadata['address']}")


        st.success("Data successfully retrieved!")
