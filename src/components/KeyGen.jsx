import React, { useState } from "react";
import { ConnectWallet, useAddress } from "@thirdweb-dev/react";
import { useParams } from "react-router-dom";

const KeyGen = () => {
  const address = useAddress(); // Get the connected wallet address
  const { token } = useParams(); // Get the token from the URL
  const [status, setStatus] = useState(""); // To display status messages

  const handleGenerateKey = async () => {
    if (!address || !token) {
      setStatus(
        "Missing token or wallet address. Please connect your wallet or check the URL."
      );
      return;
    }

    try {
      // Call the FastAPI backend
      const response = await fetch("http://localhost:8000/api/setKey", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          token: token,
          public_address: address,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setStatus("Key generated successfully: " + JSON.stringify(data));
      } else {
        setStatus("Error: " + data.detail);
      }
    } catch (error) {
      console.error("Network error:", error);
      setStatus("Network error: Unable to connect to the server.");
    }
  };

  return (
    <div>
      {/* Connect Wallet Button */}
      <div className="connect_btn">
        <ConnectWallet btnTitle="Login/Signup" />
      </div>

      {/* Display Token and Address */}
      <p>
        <b>Token:</b> {token || "Token not found in URL"}
      </p>
      <p>
        <b>Wallet Address:</b> {address || "Please connect your wallet"}
      </p>

      {/* Generate Key Button */}
      {address && token && (
        <button
          onClick={handleGenerateKey}
          style={{ padding: "10px 20px", marginTop: "20px" }}
        >
          Generate Key
        </button>
      )}

      {/* Status Message */}
      {status && <p style={{ marginTop: "20px", color: "blue" }}>{status}</p>}
    </div>
  );
};

export default KeyGen;
