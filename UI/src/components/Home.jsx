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
  const [userId, setUserId] = useState("");
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
          setAccount(accounts[0]);
          const userId = await contract.getBlockId(accounts[0]);
          setUserId(userId);
        } else {
          alert("Please install MetaMask or a Web3 provider.");
        }
      } catch (error) {
        console.log(error);
      }
    };

    connectWallet();
  }, []);
  console.log(account, userId);
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

      {account && userId && (
        <>
          <iframe
            src={`http://localhost:8501/?public_address=${account}&userId=${userId}`}
            style={{ width: "100vw", height: "100vh", border: "none" }}
            title="User Dashboard"
          ></iframe>
        </>
      )}
    </>
  );
};

export default Home;
