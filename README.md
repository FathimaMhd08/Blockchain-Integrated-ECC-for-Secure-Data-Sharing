# Blockchain-Integrated Elliptic Curve Cryptography for Secure Data Sharing

A secure document sharing system that combines **Blockchain**, **Elliptic Curve Cryptography (ECC)**, and **SHA-256 hashing** to verify file integrity and authenticate file transfers.

## Project Overview

This project is designed to provide a secure way to share documents between a sender and a receiver.

The system uses cryptographic techniques to generate digital signatures for files and stores transaction information in a blockchain-based ledger. When the receiver receives a file, the system verifies its integrity and authenticity before allowing the verified file to be downloaded.

The project is implemented using **Python in Google Colab** with **Google Drive** for cloud-based storage.

## Key Features

- 🔐 ECC-based cryptographic key generation
- ✍️ ECDSA digital signatures using SECP256k1
- 🔎 SHA-256 file hashing
- ⛓️ Blockchain-based transaction ledger
- ⛏️ Proof-of-Work block mining
- 📁 Secure file upload and storage
- ☁️ Google Drive integration
- 🛡️ File integrity verification
- ✅ Digital signature verification
- 👤 Sender and receiver verification
- 📥 Automatic download of verified files
- 📋 Blockchain transaction viewer
- 📝 System activity logging

## Technologies Used

- **Python**
- **Google Colab**
- **Elliptic Curve Cryptography (ECC)**
- **ECDSA**
- **SECP256k1**
- **SHA-256**
- **Blockchain**
- **Proof-of-Work (PoW)**
- **Google Drive**
- **IPyWidgets**
- **JSON**

## System Workflow

The system works through three main components:

### 1. Sender

The sender performs the following steps:

1. Uploads a file.
2. Enters the sender and receiver information.
3. Generates an ECC private key and public key.
4. Calculates the SHA-256 hash of the file.
5. Creates a digital signature using the private key.
6. Stores the file and transaction information.
7. Adds the transaction to the blockchain.
8. Mines a new block using Proof-of-Work.

The blockchain transaction stores information such as the sender, receiver, file name, file hash, digital signature, public key, and timestamp.

### 2. Receiver

The receiver performs the following steps:

1. Enters the file name.
2. Provides the sender's public key.
3. Uploads the received file.
4. Searches for the corresponding transaction in the blockchain.
5. Calculates the SHA-256 hash of the received file.
6. Compares the received hash with the hash stored in the blockchain.
7. Verifies the digital signature using the sender's public key.
8. Downloads the file if all verification checks are successful.

### 3. Blockchain Explorer

The blockchain viewer allows users to:

- View the complete blockchain ledger.
- View individual blocks.
- View block hashes.
- View previous block hashes.
- View timestamps and nonces.
- View stored file transactions.
- Refresh the blockchain information.

## Security Verification

The receiver performs multiple checks before accepting a file.

### File Integrity Verification

The SHA-256 hash of the received file is calculated and compared with the hash stored in the blockchain.

If the hashes are different, the system identifies a possible modification or tampering of the file.

### Digital Signature Verification

The system verifies the digital signature using the sender's public key.

If the signature is valid, the file can be authenticated against the recorded transaction.

### Blockchain Verification

The system searches the blockchain ledger for the file transaction before performing the remaining verification steps.

If no matching transaction is found, the verification process fails.

## Cryptographic Process

The project uses the following cryptographic workflow:

```text
File
  ↓
SHA-256 Hash
  ↓
ECC Digital Signature
  ↓
Blockchain Transaction
  ↓
Proof-of-Work Mining
  ↓
Blockchain Ledger
```

During verification:
```
Received File
     ↓
SHA-256 Hash
     ↓
Compare with Blockchain Hash
     ↓
Verify Digital Signature
     ↓
Verification Successful
```

## Blockchain Structure
Each block contains information including:
- Block index
- Transactions
- Timestamp
- Previous block hash
- Current block hash
- Nonce
The block hash is calculated using SHA-256, and Proof-of-Work is used during block mining.

## Google Drive Integration
Google Drive is used to organize and store project data.
The system creates separate directories for:
```
SecureDocumentSharing/
│
├── blockchain_data/
├── cryptographic_keys/
├── shared_files/
└── system_logs/
```
The project stores blockchain backups, cryptographic key information, shared files, and system activity logs in these directories.

## Requirements
The project is designed to run in Google Colab.
Required components include:
- Python 3.8+
- Google Colab
- Google Drive
- ecdsa
- ipywidgets

## Installation

Install the required ECDSA package in Google Colab:
```bash
pip install ecdsa
```
The project also uses Google Colab's built-in modules and IPyWidgets.

## How to Run
1. Open the project in Google Colab.
2. Run the installation/import section.
3. Connect your Google Drive when prompted.
4. Run the project cells.
5. The Secure Document Sharing System interface will appear.
6. Use the available Sender, Receiver, and Blockchain tabs.

## How to Use

### Sender
1. Open the Sender tab.
2. Click Upload File.
3. Select the file to be shared.
4. Enter the sender name.
5. Enter the receiver name.
6. Click Generate Keys & Sign.
7. Save the generated private key securely.
8. Share the public key and required file information with the receiver.
9. Click Store to Blockchain.

### Receiver
1. Open the Receiver tab.
2. Enter the exact file name.
3. Enter the sender's public key.
4. Upload the received file.
5. Click Verify & Download.
6. The system checks the blockchain transaction.
7. The system verifies the file hash.
8. The system verifies the digital signature.
9. If verification succeeds, the verified file is automatically downloaded.

## Project Structure
```
Blockchain-Secure-Data-Sharing/
│
└── blockchain_project.py
```

## Main Modules
**ECC Manager**
Responsible for:
- Generating ECC key pairs
- Creating digital signatures
- Verifying digital signatures

**Blockchain**
Responsible for:
- Creating the genesis block
- Adding file transactions
- Mining blocks
- Maintaining the blockchain ledger
- Saving blockchain backups

**Sender Module**
Responsible for:
- File upload
- Key generation
- SHA-256 hashing
- Digital signing
- Blockchain transaction creation

**Receiver Module**
Responsible for:
- Received file upload
- Blockchain transaction lookup
- Hash verification
- Digital signature verification
- Verified file download

**Blockchain Explorer**
Responsible for displaying:
- Blocks
- Hashes
- Previous hashes
- Timestamps
- Nonces
- File transactions

## Security Benefits
The combination of hashing, digital signatures, and blockchain provides multiple verification mechanisms:
- SHA-256 helps detect changes to file contents.
- Digital signatures provide a mechanism to verify the signer.
- Blockchain records maintain transaction information in a linked ledger.
- Proof-of-Work is used when adding blocks to the ledger.
- Public-key verification allows the receiver to verify the digital signature.

## Important Security Note
The private key is sensitive information and must be kept confidential.
The project displays a warning to save the private key because it is required for future signature verification.
Do not share the private key with other users.

## Project Objective
The main objective of this project is to develop a secure document sharing system that combines cryptographic verification with blockchain-based transaction recording.
The system demonstrates how ECC digital signatures, SHA-256 hashing, and blockchain technology can work together to verify file integrity and authenticity during document sharing.

## Future Enhancements
Possible future improvements include:
- Implementing a distributed blockchain network
- Adding user authentication
- Adding role-based access control
- Improving key management and secure key storage
- Adding encrypted file storage
- Developing a web-based deployment
- Adding database integration
- Implementing stronger blockchain consensus mechanisms
- Adding multi-user and multi-node support

## Disclaimer
This project is developed for academic and educational purposes. It demonstrates the concepts of cryptographic signatures, hashing, blockchain, and secure file verification.
It should not be considered a production-ready secure file-sharing platform without additional security testing, key-management controls, authentication, encryption, and deployment hardening.

## Author
**Syed Ali Fathima**
B.Tech - Cyber Security
