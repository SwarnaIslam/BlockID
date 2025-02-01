import streamlit as st
from web3 import Web3
from abi.BlockID import blockABI
from abi.BlockTRX import blockTRX
import requests
import hashlib
import base64
from cryptography.fernet import Fernet
import tenseal as ts

ID_RPC_URL = st.secrets["subnet"]["ID_RPC_URL"]
TRX_RPC_URL = st.secrets["subnet"]["TRX_RPC_URL"]
ID_ADDRESS = st.secrets["contract"]["BLOCKID"]
TRX_ADDRESS = st.secrets["contract"]["BLOCKTRX"]

# Web3 Initialization
id_w3 = Web3(Web3.HTTPProvider(ID_RPC_URL))
trx_w3 = Web3(Web3.HTTPProvider(TRX_RPC_URL))
ID_ADDRESS = Web3.to_checksum_address(ID_ADDRESS)
TRX_ADDRESS = Web3.to_checksum_address(TRX_ADDRESS)

id_contract = id_w3.eth.contract(address=ID_ADDRESS, abi=blockABI)
trx_contract = trx_w3.eth.contract(address=TRX_ADDRESS, abi=blockTRX)

def get_metadata_from_ipfs(cid: str):
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def decrypt_fhe_private_key(encrypted_private_key: bytes, password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()  # Generate a 32-byte key
    fernet_key = base64.urlsafe_b64encode(key)  # Convert to Fernet-compatible key
    fernet = Fernet(fernet_key)
    return fernet.decrypt(encrypted_private_key)

def decode_base64(data: bytes) -> bytes:
    return base64.b64decode(data)

import json
import os

# Path to the JSON file storing the last nonce
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

def set_cid_to_result(public_key: str, private_key: str, result: str):
    try:
        latest_nonce = get_last_nonce() + 1
        
        txn = trx_contract.functions.setCidToResult(cid, result).build_transaction({
            'from': public_key,
            'nonce': latest_nonce,
            'gas': 200000, 
            'gasPrice': id_w3.to_wei('30', 'gwei')  
        })

        signed_txn = trx_w3.eth.account.sign_transaction(txn, private_key=private_key)

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
        st.error(f"Error while setting CID to result: {e}")
        return None

password = st.text_input("User Password", type="password", placeholder="Enter the password")
private_address = st.text_input("User Private Address", type="password", placeholder="Enter the private Address")

cid = st.query_params["cid"]
public_address = st.query_params["public_address"]

if cid and public_address and password and private_address:
    public_address = Web3.to_checksum_address(public_address)

    user_id = id_contract.functions.getBlockId(public_address).call()

    metadata = get_metadata_from_ipfs(user_id)
    fhe_private_key_cid = metadata.get("fhe_private_key")
    
    encrypted_distance_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    encrypted_distance_data = requests.get(encrypted_distance_url).content

    if fhe_private_key_cid:
        fhe_private_key_url = f"https://gateway.pinata.cloud/ipfs/{fhe_private_key_cid}"
        encrypted_fhe_private_key = requests.get(fhe_private_key_url).content

        try:
            decrypted_fhe_private_key = decrypt_fhe_private_key(encrypted_fhe_private_key, password)

            context = ts.context_from(decrypted_fhe_private_key)

            encrypted_vector = ts.lazy_ckks_vector_from(decode_base64(encrypted_distance_data))
            encrypted_vector.link_context(context)
            result = encrypted_vector.decrypt()[0]
            # st.write(result)
            if result <= 15:
                st.success("Verified")
            else:
                st.warning("Not Verified")

            set_cid_to_result(public_address, private_address, str(result))
        except Exception as e:
            st.error(f"Failed to process decryption: {e}")
    else:
        st.error("Metadata is missing required fields (fhe_private_key or encrypted_distance).")

