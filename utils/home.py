import streamlit as st
import requests
from datetime import datetime
import tenseal as ts
from deepface import DeepFace
from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import base64
import hashlib

PINATA_API_KEY = st.secrets["pinata"]["api_key"]
PINATA_SECRET_API_KEY = st.secrets["pinata"]["secret_key"]
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/"
st.set_page_config(page_title="User Information Form", layout="centered")

st.title("User Information Form")
st.subheader("Please fill out the form below")

public_address=st.query_params["public_address"]

def write_data(file_name, data):
    with open(file_name, 'wb') as f:
        f.write(data)
def generate_fhe_key_pair():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.generate_galois_keys()
    context.global_scale = 2**40
    
    secret_context = context.serialize(save_secret_key=True)
    
    context.make_context_public()
    public_context = context.serialize()
    write_data("public_key.txt", public_context)
    
    return secret_context, public_context

def upload_file_to_pinata(file_path: str):
    url = PINATA_BASE_URL + "pinFileToIPFS"
    
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    with open(file_path, "rb") as file:
        files = {
            "file": file
        }
        response = requests.post(url, headers=headers, files=files)
    
    return response.json()['IpfsHash']

def create_pin_group(name:str, dob:str, address:str, cid_list: list):
    url = PINATA_BASE_URL + "pinJSONToIPFS"
    
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    data = {
        "fhe_public_key":cid_list[0],
        "fhe_private_key":cid_list[1],
        "encrypted_image":cid_list[2],
        "name":name,
        "dob":dob,
        "address":address
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    return response.json()['IpfsHash']

def encrypt_fhe_private_key(private_key: bytes, password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()  # Hash the password to get a 32-byte key
    fernet_key = base64.urlsafe_b64encode(key)  # Convert to Fernet-compatible key

    # Encrypt the private key
    fernet = Fernet(fernet_key)
    encrypted_private_key = fernet.encrypt(private_key)

    return encrypted_private_key

with st.form("user_form", clear_on_submit=False):
    st.write("### Personal Details")
    
    name = st.text_input("Name", placeholder="Enter your full name") 
    dob = st.date_input("Date of Birth", value=datetime(2000, 1, 1))  
    address = st.text_area("Current Address", placeholder="Enter your current address")
    
    st.write("### Security Details")
    
    face_image = st.file_uploader("Upload a clear image of user's face", type=["jpg", "jpeg", "png"])  
    st.write("### Password Setup")

    st.warning("Please create a strong password and remember it! You cannot recover this password if you forget it.")

    password = st.text_input(
        "Set a Password (Minimum 8 characters with letters, numbers, and special characters)",
        type="password",
        placeholder="Enter a strong password",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your password",
    )
    
    submitted = st.form_submit_button("Submit")
    
if submitted:
    if not name or not address or not public_address or not face_image or not password or not confirm_password:
        st.error("Please fill out all fields, including the password fields.")
    elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or not any(not char.isalnum() for char in password):
        st.error("Your password must be at least 8 characters long, include letters, numbers, and special characters.")
    elif password != confirm_password:
        st.error("Passwords do not match. Please try again.")
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("### User Information:")
            st.write(f"**Name:** {name}")
            st.write(f"**Date of Birth:** {dob.strftime('%d %B, %Y')}")
            st.write(f"**Address:** {address}")
            st.write(f"**Public Address:** {public_address}")

        with col2:
            st.image(face_image, caption="Uploaded Image")

        # Show processing status
        with st.status("Processing... This may take a moment."):
            secret_context, public_context = generate_fhe_key_pair()
            encrypted_secret_context = encrypt_fhe_private_key(secret_context, password)
            write_data("encrypted_secret_key.txt", encrypted_secret_context)
            public_context = ts.context_from(public_context)

            image = Image.open(face_image)
            if image.mode == "RGBA":
                image = image.convert("RGB")

            temp_image_path = "temp_image.jpg"
            image.save(temp_image_path, format="JPEG")

            embedding = DeepFace.represent(temp_image_path, model_name="Facenet")[0]["embedding"]
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()

            enc_embedding = ts.ckks_vector(public_context, embedding)
            encrypted_data = enc_embedding.serialize()
            write_data("encrypted_face_embedding.txt", encrypted_data)

            public_cid = upload_file_to_pinata("public_key.txt")
            private_cid = upload_file_to_pinata("encrypted_secret_key.txt")
            image_cid = upload_file_to_pinata("encrypted_face_embedding.txt")

            group_cid = create_pin_group(name, dob.isoformat(), address, [public_cid, private_cid, image_cid])
            # group_cid=1234
        st.success(f"Processing complete! **Generated User ID:** {group_cid}")
