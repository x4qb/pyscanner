const { ethers } = require('ethers');
let walletAddress = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e';
const ethProvider = ethers.getDefaultProvider('homestead');

async function getInfoFromWallet(address) {
  try {
    const balance = await provider.getBalance(address);
    console.log(`Balance: ${ethers.utils.formatEther(balance)} ETH`);
  } catch (err) {
    console.error("Error fetching balance:", err);
  }
}

getWalletInfo(address);