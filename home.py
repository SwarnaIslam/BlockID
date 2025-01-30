import streamlit as st
import tenseal as ts
import base64
import requests
from deepface import DeepFace
from PIL import Image
import numpy as np
from web3 import Web3
from abi.BlockID import blockABI
from abi.BlockTRX import blockTRX
import os
import json

PINATA_API_KEY = st.secrets["pinata"]["api_key"]
PINATA_SECRET_API_KEY = st.secrets["pinata"]["secret_key"]
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/"

sp_private_address=st.secrets["wallet"]["private_address"]
sp_public_address=st.secrets["wallet"]["public_address"]
ID_RPC_URL=st.secrets["subnet"]["ID_RPC_URL"]
TRX_RPC_URL=st.secrets["subnet"]["TRX_RPC_URL"]
ID_ADDRESS=st.secrets["contract"]["BLOCKID"]
TRX_ADDRESS=st.secrets["contract"]["BLOCKTRX"]

id_w3 = Web3(Web3.HTTPProvider(ID_RPC_URL))
trx_w3 = Web3(Web3.HTTPProvider(TRX_RPC_URL))
ID_ADDRESS = Web3.to_checksum_address(ID_ADDRESS)
TRX_ADDRESS = Web3.to_checksum_address(TRX_ADDRESS)
id_contract = id_w3.eth.contract(address=ID_ADDRESS, abi=blockABI)
trx_contract = trx_w3.eth.contract(address=TRX_ADDRESS, abi=blockTRX)


def write_data(file_name, data):
    with open(file_name, 'wb') as f:
        f.write(base64.b64encode(data))

def upload_file_to_pinata(file_path: str):
    url = PINATA_BASE_URL + "pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
    }

    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, headers=headers, files=files)
    return response.json()['IpfsHash']

def get_metadata_from_ipfs(cid: str):
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
NONCE_FILE_PATH = "nonce.json"

def get_last_nonce():
    if os.path.exists(NONCE_FILE_PATH):
        with open(NONCE_FILE_PATH, "r") as f:
            data = json.load(f)
            return data.get("last_nonce", 0)  
    else:
        return 0 

def update_nonce(new_nonce):
    with open(NONCE_FILE_PATH, "w") as f:
        json.dump({"last_nonce": new_nonce}, f)
def set_cid_to_address(cid: str):
    try:
        latest_nonce = get_last_nonce() + 1
        txn = trx_contract.functions.setCidToAddress(public_address, cid).build_transaction({
            'from': sp_public_address,
            'nonce': latest_nonce,
            'gas': 200000, 
            'gasPrice': id_w3.to_wei('30', 'gwei')  
        })

        signed_txn = trx_w3.eth.account.sign_transaction(txn, private_key=sp_private_address)

        tx_hash = trx_w3.eth.send_raw_transaction(signed_txn.raw_transaction)  

        tx_receipt = trx_w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_info = {
            'Transaction Hash': tx_receipt['transactionHash'].hex(),
            'Block Number': tx_receipt['blockNumber'],
            'Status': 'Success' if tx_receipt['status'] == 1 else 'Failure',
            'Gas Used': tx_receipt['gasUsed'],
            'Effective Gas Price': tx_receipt['effectiveGasPrice'],
            'From': tx_receipt['from'],
            'To': tx_receipt['to']
        }
        st.write(tx_info)
        update_nonce(latest_nonce)
        return tx_receipt
    except Exception as e:
        st.error(f"Transaction Error: {e}")
        return None

st.title("User Verification")

public_address = st.text_input("User Public Address", placeholder="Enter the user public address")
uploaded_image = st.file_uploader("Upload a new image for encryption", type=["jpg", "jpeg", "png"])

if st.button("Process and Upload"):
    if not public_address or not uploaded_image:
        st.error("Please provide public address and upload an image.")
    else:
        try:
            public_address = Web3.to_checksum_address(public_address)
            user_id = id_contract.functions.getBlockId(public_address).call()
            st.info(f"Fetching metadata from IPFS...{user_id}")
            
            metadata = get_metadata_from_ipfs(user_id)
            public_key_cid = metadata.get("fhe_public_key")
            encrypted_image_cid = metadata.get("encrypted_image")

            public_key_url = f"https://gateway.pinata.cloud/ipfs/{public_key_cid}"
            public_key_data = requests.get(public_key_url, stream=True).content
            public_context = ts.context_from(public_key_data)

            encrypted_image_url = f"https://gateway.pinata.cloud/ipfs/{encrypted_image_cid}"
            encrypted_image_data = requests.get(encrypted_image_url, stream=True).content
            enc_image_vector = ts.lazy_ckks_vector_from(encrypted_image_data)
            enc_image_vector.link_context(public_context)

            image = Image.open(uploaded_image)
            if image.mode == "RGBA":
                image = image.convert("RGB")
            temp_image_path = "uploaded_image.jpg"
            image.save(temp_image_path, format="JPEG")

            image_embedding = DeepFace.represent(temp_image_path, model_name="Facenet")[0]["embedding"]
            enc_uploaded_image = ts.ckks_vector(public_context, image_embedding)

            euclidean_squared = enc_image_vector - enc_uploaded_image
            euclidean_squared = euclidean_squared.dot(euclidean_squared)

            encrypted_distance_data = euclidean_squared.serialize()
            distance_file_path = "encrypted_distance.txt"
            write_data(distance_file_path, encrypted_distance_data)

            distance_cid = upload_file_to_pinata(distance_file_path)
            # distance_cid="QmfL2dY1aNmMztxzRFJuzWfYkXALgrKHJUyjcAsagT3HFd"

            set_cid_to_address(distance_cid)

            destination_url = f"http://localhost:8501/?cid={distance_cid}&public_address={public_address}"
            st.markdown(f"[Go to the next page to submit confidential info]( {destination_url} )", unsafe_allow_html=True)


        except Exception as e:
            st.error(f"An error occurred: {e}")
