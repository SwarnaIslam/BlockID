import React from "react";
import { ConnectWallet } from "@thirdweb-dev/react";
import "./index.css";
const Login = () => {
  return (
    <>
      <div className="connect_btn">
        <ConnectWallet btnTitle="Login/Signup" />
      </div>
    </>
  );
};

export default Login;
