# **BlockID: Secure Blockchain-Based Identity Management System**

BlockID is a **decentralized identity management system** leveraging **Avalanche Subnets** for secure, transparent, and user-controlled identity verification. This project is based on the research paper:

📄 **M. A. R. Tonu, S. Hridoy, M. A. Ali, and S. A. Azad**,  
*"Block - NID: A Conceptual Secure Blockchain-Based National Identity Management System Model,"*  
**2019 IEEE Asia-Pacific Conference on Computer Science and Data Engineering (CSDE)**  
[DOI: 10.1109/CSDE48274.2019.9162366](https://doi.org/10.1109/CSDE48274.2019.9162366)

## **Project Overview**
This project introduces two **Avalanche Subnets**:
- **BlockID** 🏛️ → For storing and managing identity-related data.  
- **BlockTRX** 💳 → For handling transactions between users.  

It ensures **secure data storage** (via **IPFS**), **privacy** (**Fully Homomorphic Encryption - FHE**), and **decentralization** (**Avalanche Subnets**).

---

## **1️⃣ Cloning the Project**
```bash
git clone -b subnet https://github.com/your-repo/blockid.git
cd blockid
```

---

## **2️⃣ Setting Up Avalanche Subnets**
My avalanche version is 1.8.4

### **Create Two Separate Subnets**
#### **➡️ Create BlockID Subnet**
```bash
avalanche blockchain create BlockID --sovereign=false
```
📌 **Configuration for BlockID**  
- **VM Type:** `Subnet-EVM`  
- **Validator Management:** `Proof of Authority`  
- **Controller Address:** `ewoq` (or an imported key)  
- **Chain ID:** `5555`  
- **Token Symbol:** `BID`  
- **Transaction Allow List:** `ON`  
- **Smart Contract Deployment:** `Restricted to approved addresses`

#### **➡️ Create BlockTRX Subnet**
```bash
avalanche blockchain create BlockTRX --sovereign=false
```
📌 **Configuration for BlockTRX**  
- **VM Type:** `Subnet-EVM`  
- **Chain ID:** `9999`  
- **Token Symbol:** `TRX`  
- **Transaction Allow List:** `OPEN (anyone can transact)`  
- **Smart Contract Deployment:** `Restricted to approved addresses`

### **Deploy the Subnets**
```bash
avalanche blockchain deploy BlockID
avalanche blockchain deploy BlockTRX
```
Copy the **RPC URLs** generated for **BlockID** and **BlockTRX**.

---

## **3️⃣ Deploy Smart Contracts**
### **Create a `.env` file**
```ini
id_rpc_url=your_rpc_url_for_block_id
trx_rpc_url=your_rpc_url_for_block_trx
private_key=your_private_key
```
Source the `.env` file:
```bash
source .env
```
### **Deploy Contracts**
#### **➡️ Deploy BlockID Smart Contract**
```bash
forge script script/DeployBlockID.s.sol --rpc-url $id_rpc_url --broadcast --private-key $private_key
```
#### **➡️ Deploy BlockTRX Smart Contract**
```bash
forge script script/DeployBlockTRX.s.sol --rpc-url $trx_rpc_url --broadcast --private-key $private_key
```
Copy the contract **addresses** and **ABIs**.

---

## **4️⃣ Add Subnets to Avalanche Core Wallet**
1. Open **Avalanche Core Wallet**.  
2. Click **Add Custom Network** and enter:
   - **BlockID RPC URL**  
   - **BlockTRX RPC URL**  
3. Import the **admin/manager accounts** created in the subnet.  
4. Transfer dummy **BID** and **TRX** tokens from the `ewoq` account.

---

## **5️⃣ Set Up the UI**
Clone the UI repository:
```bash
git clone -b main https://github.com/your-repo/blockid-ui.git
cd blockid-ui
```
Create an `.env` file:
```ini
VITE_CONTRACT_ADDRESS=contract_address_of_BlockID
```
Install dependencies:
```bash
npm install
```
Run the UI:
```bash
npm run dev
```

---

## **6️⃣ Set Up Backend Utilities**
Clone the backend utilities repository:
```bash
git clone -b utils https://github.com/your-repo/blockid-utils.git
cd blockid-utils
```
Create a `.streamlit/secrets.toml` file:
```ini
[pinata]
secret_key = "your_pinata_secret_key"
api_key = "your_pinata_api_key"
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the backend:
```bash
streamlit run home.py
```

---

## **7️⃣ Additional Modules**
### **➡️ SP_UI (Service Provider Verification)**
```bash
git clone -b SP_UI https://github.com/your-repo/sp-ui.git
cd sp-ui
```
Create `.streamlit/secrets.toml`:
```ini
[wallet]
public_address = "your_public_address"
private_address = "your_private_address"

[subnet]
ID_RPC_URL = "your_blockid_rpc_url"
TRX_RPC_URL = "your_blocktrx_rpc_url"

[contract]
BLOCKID = "contract_address_of_BlockID"
BLOCKTRX = "contract_address_of_BlockTRX"
```
Install and run:
```bash
pip install -r requirements.txt
streamlit run home.py
```

---

### **➡️ V_UI (Verification Interface)**
```bash
git clone -b V_UI https://github.com/your-repo/v-ui.git
cd v-ui
```
Create `.streamlit/secrets.toml`:
```ini
[subnet]
ID_RPC_URL = "your_blockid_rpc_url"
TRX_RPC_URL = "your_blocktrx_rpc_url"

[contract]
BLOCKID = "contract_address_of_BlockID"
BLOCKTRX = "contract_address_of_BlockTRX"
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the service:
```bash
streamlit run home.py
```

---

### **➡️ User_UI (User Dashboard)**
```bash
git clone -b User_UI https://github.com/your-repo/user-ui.git
cd user-ui
```
Create an `.env` file:
```ini
VITE_CONTRACT_ADDRESS=contract_address_of_BlockID
```
Install dependencies:
```bash
npm install
```
Run the UI:
```bash
npm run dev
```

---

## **🎯 Final Steps**
Ensure the following are running:
✅ **Avalanche Subnets (BlockID & BlockTRX)**  
✅ **Smart Contracts Deployed**  
✅ **UI Interfaces (User, SP, Verification)**  
✅ **Backend Services (IPFS, Streamlit, Pinata)**  

You can now interact with **BlockID** using the User Dashboard and Service Provider Verification.

---

## **📜 License**
This project is released under the **MIT License**.

## **👥 Contributors**
- **Swarna Islam** - *Lead Developer*
- **Supervised by:** Dr. Sumon Ahmed, **Associate Professor, IIT, University of Dhaka**

