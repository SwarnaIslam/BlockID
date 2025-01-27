// App.js or App.tsx
import React from "react";
import { ThirdwebProvider, ChainId, coreWallet } from "@thirdweb-dev/react";
import Login from "./Login";
import { Route, Routes } from "react-router-dom";
import KeyGen from "./components/KeyGen";
const App = () => {
  const LOCAL_CHAIN = {
    chainId: 5555,
    rpc: [
      "http://127.0.0.1:36409/ext/bc/Pa5ZwerC9xNqR3UUdKxaTciGE2Bc2GTh5hubGQkHTrxbUw8fp/rpc",
    ],
    nativeCurrency: {
      name: "BID Token",
      symbol: "BID",
      decimals: 18,
    },
    shortName: "avalanche-local",
    slug: "avalanche-local",
    explorers: [],
    name: "BlockID",
  };
  return (
    <ThirdwebProvider
      activeChain={LOCAL_CHAIN}
      supportedWallets={[coreWallet()]}
    >
      <Login />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/keygen/:token" element={<KeyGen />} />
      </Routes>
    </ThirdwebProvider>
  );
};

export default App;
