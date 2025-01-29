import React, { useState, useEffect } from "react";
import "../css/general.css";
import abi from "../contract/BlockID.json";
import { ethers } from "ethers";
import { Form, InputGroup, Button } from "react-bootstrap";
const Home = () => {
  const [state, setState] = useState({
    provider: null,
    signer: null,
    contract: null,
  });
  const [account, setAccount] = useState(null);
  const [publicAddress, setPublicAddress] = useState("");
  const [publicTempAddress, setpublicTempAddress] = useState("");
  const [userId, setUserId] = useState("");
  const addUser = async () => {
    const { contract } = state;
    try {
      console.log(publicAddress + " " + userId);
      const tx = await contract.setBlockId(publicAddress, userId);
      await tx.wait();

      console.log("Transaction successful:", tx.hash);

      contract.on("BlockIdSet", (user, blockId, event) => {
        alert(`User Added: User=${user}, BlockId=${blockId}`);
      });
    } catch (error) {
      console.error("Transaction failed:", error);
      alert("Transaction failed. Check the console for details.");
    }
  };
  const getUser = async () => {
    const { contract } = state;

    try {
      console.log(publicAddress);
      const blockId = await contract.getBlockId(publicAddress);

      console.log("Block ID for the user:", blockId);
      alert(`Block ID: ${blockId}`);
    } catch (error) {
      console.error("Error fetching Block ID:", error);
      alert("Failed to fetch Block ID. Check the console for details.");
    }
  };
  useEffect(() => {
    const connectWallet = async () => {
      const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
      const contractABI = abi.abi;
      try {
        const { ethereum } = window;
        if (ethereum) {
          const accounts = await ethereum.request({
            method: "eth_requestAccounts",
          });

          window.ethereum.on("chainChanged", () => {
            window.location.reload();
          });
          window.ethereum.on("accountsChanged", () => {
            window.location.reload();
          });

          const provider = new ethers.providers.Web3Provider(ethereum);
          const signer = provider.getSigner();
          const contract = new ethers.Contract(
            contractAddress,
            contractABI,
            signer
          );

          setState({ provider, signer, contract });
          setAccount(accounts[0]); // Set first connected account
        } else {
          alert("Please install MetaMask or a Web3 provider.");
        }
      } catch (error) {
        console.log(error);
      }
    };

    connectWallet();
  }, []);
  useEffect(() => {
    if (publicTempAddress === "") {
      setPublicAddress("");
    }
  }, [publicTempAddress]);
  return (
    <>
      <nav className="navbar navbar-dark bg-dark d-flex px-3">
        <a className="navbar-brand" href="#">
          <img
            src="/images/blockID.png"
            width="30"
            height="30"
            className="d-inline-block align-top"
            alt="BlockID"
          />
          BlockID
        </a>
        <div className="ms-auto">
          {account ? (
            <span className="text-light">
              <span
                className="me-2"
                style={{
                  display: "inline-block",
                  width: "10px",
                  height: "10px",
                  backgroundColor: "#3fff00",
                  borderRadius: "50%",
                }}
              ></span>
              {account.slice(0, 6)}...{account.slice(-4)}
            </span>
          ) : (
            <button
              className="btn btn-outline-danger"
              onClick={() => window.location.reload()}
            >
              <span
                style={{
                  display: "inline-block",
                  width: "10px",
                  height: "10px",
                  backgroundColor: "red",
                  borderRadius: "50%",
                  marginRight: "8px",
                }}
              ></span>
              Connect
            </button>
          )}
        </div>
      </nav>
      <div className="d-flex justify-content-center align-items-center mt-3">
        <InputGroup style={{ maxWidth: "400px" }}>
          <Form.Control
            type="text"
            placeholder="Enter User public address"
            value={publicTempAddress}
            onChange={(e) => setpublicTempAddress(e.target.value)}
          />
        </InputGroup>
        <Button
          variant="primary"
          onClick={() => {
            setPublicAddress(publicTempAddress);
          }}
          className="ms-2"
        >
          Initiat Process
        </Button>
      </div>
      {publicAddress && (
        <>
          <iframe
            src={`http://localhost:8501/?public_address=${publicAddress}`}
            style={{ width: "100vw", height: "100vh", border: "none" }}
            title="Streamlit Dashboard"
          ></iframe>
          <div className="d-flex justify-content-center align-items-center mt-3">
            <InputGroup style={{ maxWidth: "400px" }}>
              <Form.Control
                type="text"
                placeholder="Enter the User ID to confirm"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
              />
            </InputGroup>
            <Button variant="primary" onClick={addUser} className="ms-2">
              Add User
            </Button>
          </div>

          <Button variant="secondary" onClick={getUser} className="mt-2">
            Get User
          </Button>
        </>
      )}
    </>
  );
};

export default Home;
