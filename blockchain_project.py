import hashlib
import json
import os
from datetime import datetime
pip install ecdsa
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
from google.colab import files
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import io
# ============================================================
# GLOBAL PREMIUM CYBER UI STYLE
# ============================================================

display(HTML("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

body {
    margin: 0 !important;
    background: #000 !important;
    font-family: 'Orbitron', sans-serif !important;
    overflow-x: hidden;
}

/* 3D Moving Grid */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(0,255,255,0.15) 0px,
            rgba(0,255,255,0.15) 1px,
            transparent 1px,
            transparent 50px
        ),
        repeating-linear-gradient(
            90deg,
            rgba(0,255,255,0.15) 0px,
            rgba(0,255,255,0.15) 1px,
            transparent 1px,
            transparent 50px
        );
    transform: perspective(900px) rotateX(65deg);
    animation: gridMove 12s linear infinite;
    z-index: -2;
}

@keyframes gridMove {
    from { transform: perspective(900px) rotateX(65deg) translateY(0px); }
    to { transform: perspective(900px) rotateX(65deg) translateY(60px); }
}

/* Glowing Cyber Energy */
body::after {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background:
        radial-gradient(circle at 20% 30%, rgba(0,255,255,0.25), transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(0,0,255,0.25), transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(0,255,150,0.25), transparent 40%);
    animation: glowPulse 6s infinite alternate;
    z-index: -1;
}

@keyframes glowPulse {
    from { opacity: 0.6; }
    to { opacity: 1; }
}

/* Tabs Styling */
.jupyter-widgets .p-TabBar-tab {
    font-weight: bold !important;
    font-size: 14px !important;
    background: linear-gradient(145deg,#1e3c72,#2a5298) !important;
    color: white !important;
    border-radius: 10px 10px 0 0 !important;
}

.jupyter-widgets .p-TabBar-tab.p-mod-current {
    background: linear-gradient(145deg,#00c6ff,#0072ff) !important;
    box-shadow: 0 0 15px #00f2ff;
}

/* 3D Buttons */
button {
    border-radius: 12px !important;
    font-weight: bold !important;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4),
                inset 0 0 10px #00f2ff;
    transition: all 0.3s ease-in-out;
}

button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px #00f2ff;
}

/* Section Card */
.cyber-card {
    background: rgba(0,0,0,0.7);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #00f2ff;
    box-shadow: 0 0 25px #00f2ff44;
    margin-bottom: 20px;
}

/* Glowing Text */
.glow-text {
    color: #00f2ff;
    text-shadow: 0 0 15px #00f2ff;
}
</style>
"""))

# ============================================================================
# GOOGLE DRIVE INTEGRATION
# ============================================================================

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Create project directory in Google Drive
import os
PROJECT_DIR = '/content/drive/MyDrive/SecureDocumentSharing'
os.makedirs(PROJECT_DIR, exist_ok=True)

# Subdirectories for organized storage
BLOCKCHAIN_DIR = os.path.join(PROJECT_DIR, 'blockchain_data')
KEYS_DIR = os.path.join(PROJECT_DIR, 'cryptographic_keys')
FILES_DIR = os.path.join(PROJECT_DIR, 'shared_files')
LOGS_DIR = os.path.join(PROJECT_DIR, 'system_logs')

for directory in [BLOCKCHAIN_DIR, KEYS_DIR, FILES_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

def save_to_drive(data, filename, subdirectory=''):
    """Save data to Google Drive with organized structure"""
    if subdirectory:
        filepath = os.path.join(PROJECT_DIR, subdirectory, filename)
    else:
        filepath = os.path.join(PROJECT_DIR, filename)

    with open(filepath, 'w') as f:
        if isinstance(data, dict):
            json.dump(data, f, indent=2)
        else:
            f.write(str(data))
    return filepath

def log_activity(activity_type, details):
    """Log system activities to Google Drive"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {activity_type}: {details}\n"

    log_file = os.path.join(LOGS_DIR, f"activity_log_{datetime.now().strftime('%Y%m%d')}.txt")
    with open(log_file, 'a') as f:
        f.write(log_entry)

# ============================================================================
# CORE CLASSES
# ============================================================================

class ECCManager:
    """ECC key management and signing"""

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

        # Save keys to Google Drive
        keys_data = {
            'private_key': self.get_private_key_hex(),
            'public_key': self.get_public_key_hex(),
            'generated_at': str(datetime.now())
        }
        save_to_drive(keys_data, f"keys_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'cryptographic_keys')

        return self.get_private_key_hex(), self.get_public_key_hex()

    def get_private_key_hex(self):
        return self.private_key.to_string().hex()

    def get_public_key_hex(self):
        return self.public_key.to_string().hex()

    def sign_data(self, data_hash):
        return self.private_key.sign(data_hash).hex()

    @staticmethod
    def verify_signature(data_hash, signature_hex, public_key_hex):
        try:
            public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
            signature = bytes.fromhex(signature_hex)
            public_key.verify(signature, data_hash)
            return True
        except:
            return False


class Block:
    """Blockchain block"""

    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=2):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    """Simple blockchain for file transactions"""

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, [], str(datetime.now()), "0")
        genesis.mine_block()
        self.chain.append(genesis)

        # Save genesis block to Google Drive
        self.save_blockchain_to_drive()

    def add_transaction(self, sender, receiver, file_name, file_hash, signature, public_key):
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "file_name": file_name,
            "file_hash": file_hash,
            "signature": signature,
            "public_key": public_key,
            "timestamp": str(datetime.now())
        }
        self.pending_transactions.append(transaction)

        # Log transaction
        log_activity("TRANSACTION_ADDED", f"File: {file_name}, Sender: {sender}, Receiver: {receiver}")

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return None

        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=str(datetime.now()),
            previous_hash=self.chain[-1].hash
        )
        block.mine_block()
        self.chain.append(block)
        self.pending_transactions = []

        # Save updated blockchain to Google Drive
        self.save_blockchain_to_drive()

        # Log block mining
        log_activity("BLOCK_MINED", f"Block #{block.index} with {len(block.transactions)} transactions")

        return block

    def get_transaction(self, file_name):
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["file_name"] == file_name:
                    return transaction
        return None

    def save_blockchain_to_drive(self):
        """Save entire blockchain to Google Drive"""
        blockchain_data = []
        for block in self.chain:
            block_data = {
                "index": block.index,
                "transactions": block.transactions,
                "timestamp": block.timestamp,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
                "nonce": block.nonce
            }
            blockchain_data.append(block_data)

        save_to_drive(blockchain_data, f"blockchain_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'blockchain_data')


# ============================================================================
# GLOBAL STORAGE
# ============================================================================

blockchain = Blockchain()
uploaded_files = {}  # Store uploaded file content
ecc_manager = ECCManager()

# ============================================================================
# UI COMPONENTS AND FUNCTIONS
# ============================================================================

def create_header():
    return widgets.HTML(f"""
        <div class='cyber-card'>
            <h1 class='glow-text' style='text-align:center; font-size:36px;'>
                SECURE DOCUMENT SHARING SYSTEM
            </h1>
            <p style='text-align:center; font-weight:bold; color:white;'>
                Blockchain • ECC Digital Signature • SHA-256 • Google Drive Cloud Storage
            </p>
            <p style='text-align:center; font-size:13px; color:#ccc;'>
                Data Directory: {PROJECT_DIR}
            </p>
        </div>
    """)


def create_sender_ui():
    """Create sender interface"""

    output = widgets.Output()

    # Upload button
    upload_btn = widgets.Button(
        description='Upload File',
        button_style='primary',
        layout=widgets.Layout(width='200px', height='50px'),
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    # File info display
    file_info = widgets.HTML(value="<p style='color: #000000; font-weight: bold; text-align: center;'>No file uploaded</p>")

    # Sender name input
    sender_name = widgets.Text(
        placeholder='Enter your name (e.g., Alice)',
        description='Sender Name:',
        style={'description_width': 'initial', 'font_weight': 'bold'},
        layout=widgets.Layout(width='400px')
    )

    # Receiver name input
    receiver_name = widgets.Text(
        placeholder='Enter receiver name (e.g., Bob)',
        description='Receiver Name:',
        style={'description_width': 'initial', 'font_weight': 'bold'},
        layout=widgets.Layout(width='400px')
    )

    # Generate keys button
    generate_btn = widgets.Button(
        description='Generate Keys & Sign',
        button_style='success',
        layout=widgets.Layout(width='250px', height='50px'),
        disabled=True,
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    # Keys display
    keys_display = widgets.Accordion(children=[widgets.HTML("")])
    keys_display.set_title(0, 'Your Cryptographic Keys (Click to Expand)')
    keys_display.selected_index = None
    keys_display.layout.display = 'none'

    # Store to blockchain button
    store_btn = widgets.Button(
        description='Store to Blockchain',
        button_style='warning',
        layout=widgets.Layout(width='250px', height='50px'),
        disabled=True,
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    success_msg = widgets.HTML()

    current_file = {'name': None, 'content': None, 'hash': None, 'signature': None, 'private_key': None, 'public_key': None}

    def on_upload_click(b):
        with output:
            clear_output()
            print("Select your file to upload...")
            uploaded = files.upload()

            if uploaded:
                file_name = list(uploaded.keys())[0]
                file_content = uploaded[file_name]

                # Store file locally and in Google Drive
                uploaded_files[file_name] = file_content
                current_file['name'] = file_name
                current_file['content'] = file_content

                # Save file to Google Drive
                file_path = os.path.join(FILES_DIR, file_name)
                with open(file_path, 'wb') as f:
                    f.write(file_content)

                # Display file info
                file_size = len(file_content)
                file_info.value = f"""
                    <div style='background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 10px 0; border: 1px solid #c8e6c9; text-align: center;'>
                        <strong style='color: #000000;'>File Uploaded Successfully!</strong><br>
                        <span style='color: #000000;'><strong>File Name:</strong> {file_name}</span><br>
                        <span style='color: #000000;'><strong>File Size:</strong> {file_size} bytes</span><br>
                        <span style='color: #000000;'><strong>File ID:</strong> {file_name}_{file_size}</span><br>
                        <span style='color: #000000;'><strong>Saved to Drive:</strong> {file_path}</span>
                    </div>
                """

                generate_btn.disabled = False
                clear_output()

    def on_generate_click(b):
        if not current_file['name']:
            with output:
                clear_output()
                print("Please upload a file first!")
            return

        if not sender_name.value or not receiver_name.value:
            with output:
                clear_output()
                print("Please enter sender and receiver names!")
            return

        with output:
            clear_output()
            print("Generating ECC keys and signing file...")
            print("Please wait...")

        # Generate keys
        private_key_hex, public_key_hex = ecc_manager.generate_keys()
        current_file['private_key'] = private_key_hex
        current_file['public_key'] = public_key_hex

        # Hash file
        file_hash = hashlib.sha256(current_file['content']).digest()
        file_hash_hex = file_hash.hex()
        current_file['hash'] = file_hash_hex

        # Sign hash
        signature = ecc_manager.sign_data(file_hash)
        current_file['signature'] = signature

        # Display keys - This part is moved inside the function
        keys_display.children = [widgets.HTML(f"""
            <div style='background: #fff3e0; padding: 20px; border-radius: 8px; border: 1px solid #ffb74d; text-align: center;'>
                <p style='color: #000000; margin-bottom: 15px;'><strong>Private Key (Keep this SECRET!):</strong></p>
                <textarea readonly style='width: 100%; height: 80px; font-family: monospace; font-size: 11px; background: #fff8e1; color: #000000; border: 1px solid #ffd54f; padding: 8px; border-radius: 4px;'>{private_key_hex}</textarea>

                <p style='color: #000000; margin-top: 20px; margin-bottom: 15px;'><strong>Public Key (Share with receiver):</strong></p>
                <textarea readonly style='width: 100%; height: 80px; font-family: monospace; font-size: 11px; background: #fff8e1; color: #000000; border: 1px solid #ffd54f; padding: 8px; border-radius: 4px;'>{public_key_hex}</textarea>

                <p style='color: #000000; margin-top: 20px; margin-bottom: 15px;'><strong>File Hash (SHA-256):</strong></p>
                <textarea readonly style='width: 100%; height: 60px; font-family: monospace; font-size: 11px; background: #fff8e1; color: #000000; border: 1px solid #ffd54f; padding: 8px; border-radius: 4px;'>{file_hash_hex}</textarea>

                <p style='color: #000000; margin-top: 20px; margin-bottom: 15px;'><strong>Digital Signature (ECDSA):</strong></p>
                <textarea readonly style='width: 100%; height: 80px; font-family: monospace; font-size: 11px; background: #fff8e1; color: #000000; border: 1px solid #ffd54f; padding: 8px; border-radius: 4px;'>{signature[:200]}...</textarea>

                <div style='background: #ffebee; padding: 15px; border-radius: 5px; border: 1px solid #f44336; margin-top: 20px;'>
                    <p style='color: #c62828; margin: 0; font-weight: bold;'>SECURITY WARNING: Copy and save your Private Key immediately! You cannot recover it later. This key is required for future verification.</p>
                </div>
            </div>
        """)]
        keys_display.layout.display = 'block'

        with output:
            clear_output()
            print("Keys generated and file signed successfully!")
            print("Check 'Your Keys' section above to view and copy your keys")

        store_btn.disabled = False

    def on_store_click(b):
        if not current_file['signature']:
            with output:
                clear_output()
                print("Please generate keys first!")
            return

        with output:
            clear_output()
            print("Mining block and storing to blockchain...")

        # Add transaction
        blockchain.add_transaction(
            sender=sender_name.value,
            receiver=receiver_name.value,
            file_name=current_file['name'],
            file_hash=current_file['hash'],
            signature=current_file['signature'],
            public_key=current_file['public_key']
        )

        # Mine block
        block = blockchain.mine_pending_transactions()

        success_msg.value = f"""
            <div style='background: #c8e6c9; padding: 25px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #4caf50; border: 1px solid #81c784; text-align: center;'>
                <h3 style='margin-top: 0; color: #000000; font-weight: bold;'>Transaction Stored Successfully in Blockchain!</h3>
                <p style='color: #000000;'><strong>Block Number:</strong> {block.index}</p>
                <p style='color: #000000;'><strong>Block Hash:</strong> {block.hash[:32]}...</p>
                <p style='color: #000000;'><strong>File Name:</strong> {current_file['name']}</p>
                <p style='color: #000000;'><strong>Sender:</strong> {sender_name.value}</p>
                <p style='color: #000000;'><strong>Receiver:</strong> {receiver_name.value}</p>
                <p style='color: #000000;'><strong>Timestamp:</strong> {block.timestamp}</p>
                <p style='color: #000000;'><strong>Saved to Drive:</strong> {PROJECT_DIR}</p>

                <div style='background: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 15px; border: 1px solid #64b5f6;'>
                    <p style='color: #1976d2; margin-top: 0; font-weight: bold;'>Share the following with receiver:</strong></p>
                    <ul style='background: white; padding: 15px; border-radius: 5px; color: #000000; display: inline-block; text-align: left;'>
                        <li><strong>Public Key:</strong> Copy from 'Your Keys' section above</li>
                        <li><strong>File Name:</strong> <code style='background: #f5f5f5; padding: 2px 5px; border-radius: 3px;'>{current_file['name']}</code></li>
                        <li><strong>The Actual File:</strong> Send via email, cloud storage, or direct transfer</li>
                    </ul>
                </div>

                <div style='background: #fff3e0; padding: 12px; border-radius: 5px; margin-top: 15px; border: 1px solid #ffb74d;'>
                    <p style='color: #000000; margin: 0; font-weight: bold;'>Next Steps:</strong> The receiver should use the 'Receiver' tab to verify the file authenticity.</p>
                </div>
            </div>
        """

        with output:
            clear_output()
            print(f"Block #{block.index} mined successfully!")
            print(f"Block hash: {block.hash}")
            print(f"All data saved to Google Drive: {PROJECT_DIR}")

        # Disable buttons
        store_btn.disabled = True
        generate_btn.disabled = True

    upload_btn.on_click(on_upload_click)
    generate_btn.on_click(on_generate_click)
    store_btn.on_click(on_store_click)

    # Center-align elements in the sender UI
    centered_elements = widgets.VBox([
widgets.HTML("""
<div class='cyber-card'>
    <h2 class='glow-text' style='text-align:center;'>
        SENDER SIDE – Upload & Digitally Sign Files
    </h2>
    <p style='text-align:center; color:#ccc;'>
        Secure file transfer using ECC digital signatures and blockchain validation
    </p>
</div>
"""),
        widgets.HTML("<hr style='border: 1px solid #e0e0e0;'>"),
        widgets.HTML("<p style='color: #000000; text-align: center; font-weight: bold;'>Upload your file, generate cryptographic keys, and create a blockchain transaction.</p>"),
        widgets.HBox([upload_btn], layout=widgets.Layout(justify_content='center')),
        file_info,
        widgets.HTML("<br>"),
        widgets.HBox([sender_name], layout=widgets.Layout(justify_content='center')),
        widgets.HBox([receiver_name], layout=widgets.Layout(justify_content='center')),
        widgets.HTML("<br>"),
        widgets.HBox([generate_btn], layout=widgets.Layout(justify_content='center')),
        keys_display,
        widgets.HTML("<br>"),
        widgets.HBox([store_btn], layout=widgets.Layout(justify_content='center')),
        success_msg,
        output
    ], layout=widgets.Layout(align_items='center'))
    card_start = widgets.HTML("<div class='section-card'>")
    card_title = widgets.HTML("<div class='section-title'>SENDER SIDE - Upload & Digitally Sign Files</div>")
    card_end = widgets.HTML("</div>")
    
    return widgets.VBox([card_start, card_title, centered_elements, card_end])


def create_receiver_ui():
    """Create receiver interface"""

    output = widgets.Output()

    # File name input
    file_name_input = widgets.Text(
        placeholder='Enter exact file name',
        description='File Name:',
        style={'description_width': '100px', 'font_weight': 'bold'},
        layout=widgets.Layout(width='400px')
    )

    # Public key input
    public_key_input = widgets.Textarea(
        placeholder='Paste sender\'s public key here',
        description='Public Key:',
        style={'description_width': '100px', 'font_weight': 'bold'},
        layout=widgets.Layout(width='600px', height='100px')
    )

    # Upload received file
    upload_received_btn = widgets.Button(
        description='Upload Received File',
        button_style='info',
        layout=widgets.Layout(width='250px', height='50px'),
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    # Modified initial received_file_info for centering
    received_file_info = widgets.HTML(value="<p style='color: #000000; font-weight: bold; text-align: center;'>No file uploaded</p>")

    # Verify button
    verify_btn = widgets.Button(
        description='Verify & Download',
        button_style='success',
        layout=widgets.Layout(width='250px', height='50px'),
        disabled=True,
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    result_display = widgets.HTML()

    received_file = {'name': None, 'content': None}

    def on_upload_received_click(b):
        with output:
            clear_output()
            print("Select the file you received...")
            uploaded = files.upload()

            if uploaded:
                file_name = list(uploaded.keys())[0]
                file_content = uploaded[file_name]

                received_file['name'] = file_name
                received_file['content'] = file_content

                file_size = len(file_content)
                # Updated file_info.value to include text-align: center
                received_file_info.value = f"""
                    <div style='background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 10px 0; border: 1px solid #90caf9; text-align: center;'>
                        <strong style='color: #000000;'>Received File Uploaded!</strong><br>
                        <span style='color: #000000;'><strong>File Name:</strong> {file_name}</span><br>
                        <span style='color: #000000;'><strong>File Size:</strong> {file_size} bytes</span><br>
                        <span style='color: #000000;'><strong>Temporary ID:</strong> received_{file_name}</span>
                    </div>
                """

                verify_btn.disabled = False
                clear_output()

    def download_verified_file(file_content, filename):
        """Download the verified file automatically"""
        # Save to local Colab environment
        verified_filename = f"verified_{filename}"
        with open(verified_filename, 'wb') as f:
            f.write(file_content)

        # Save to Google Drive
        drive_filename = os.path.join(FILES_DIR, f"verified_{filename}")
        with open(drive_filename, 'wb') as f:
            f.write(file_content)

        # Trigger download
        files.download(verified_filename)

        return verified_filename, drive_filename

    def on_verify_click(b):
        if not file_name_input.value:
            with output:
                clear_output()
                print("Please enter the file name!")
            return

        if not public_key_input.value:
            with output:
                clear_output()
                print("Please enter the sender's public key!")
            return

        if not received_file['content']:
            with output:
                clear_output()
                print("Please upload the received file!")
            return

        with output:
            clear_output()
            print("Verifying file authenticity...")
            print("Step 1: Looking up transaction in blockchain...")

        # Get transaction from blockchain
        transaction = blockchain.get_transaction(file_name_input.value)

        if not transaction:
            # Updated result_display.value to include text-align: center
            result_display.value = f"""
                <div style='background: #ffebee; padding: 25px; border-radius: 10px; border-left: 5px solid #f44336; border: 1px solid #ef9a9a; text-align: center;'>
                    <h3 style='color: #000000; margin-top: 0; font-weight: bold;'>Verification Failed - Transaction Not Found</h3>
                    <p style='color: #000000;'><strong>Error Details:</strong></p>
                    <ul style='color: #000000; display: inline-block; text-align: left;'>
                        <li>No blockchain transaction found for file: <strong>{file_name_input.value}</strong></li>
                        <li>This file was never registered in the blockchain ledger</li>
                        <li>Possible causes: Wrong file name or file was not properly shared</li>
                    </ul>
                    <div style='background: #fff3e0; padding: 12px; border-radius: 5px; margin-top: 15px; border: 1px solid #ffb74d;'>
                        <p style='color: #000000; margin: 0; font-weight: bold;'>Solution: Contact the sender to ensure the file was properly uploaded and shared.</p>
                    </div>
                </div>
            """
            with output:
                clear_output()
                print("Transaction not found!")
            return

        with output:
            print("Transaction found!")
            print("Step 2: Verifying file hash integrity...")

        # Verify file hash
        received_hash = hashlib.sha256(received_file['content']).hexdigest()

        if received_hash != transaction['file_hash']:
            # Updated result_display.value to include text-align: center
            result_display.value = f"""
                <div style='background: #ffebee; padding: 25px; border-radius: 10px; border-left: 5px solid #f44336; border: 1px solid #ef9a9a; text-align: center;'>
                    <h3 style='color: #000000; margin-top: 0; font-weight: bold;'>SECURITY ALERT - File Tampering Detected!</h3>
                    <p style='color: #000000;'><strong>Security Issue:</strong> File hash does not match blockchain record</p>

                    <div style='background: white; padding: 15px; border-radius: 5px; margin: 15px 0; border: 1px solid #ffcdd2;'>
                        <p style='color: #000000; margin: 0;'><strong>Expected Hash (from blockchain):</strong></p>
                        <code style='background: #f5f5f5; padding: 8px; border-radius: 4px; display: block; margin: 5px 0; color: #000000;'>{transaction['file_hash'][:64]}...</code>

                        <p style='color: #000000; margin-top: 10px;'><strong>Actual Hash (received file):</strong></p>
                        <code style='background: #f5f5f5; padding: 8px; border-radius: 4px; display: block; margin: 5px 0; color: #000000;'>{received_hash[:64]}...</code>
                    </div>

                    <div style='background: #fff3e0; padding: 12px; border-radius: 5px; margin-top: 15px; border: 1px solid #ffb74d;'>
                        <p style='color: #000000; margin: 0; font-weight: bold;'>CRITICAL WARNING: This file has been modified after it was signed! Do not use this file as it may be malicious.</p>
                    </div>
                </div>
            """
            with output:
                clear_output()
                print("File has been tampered!")
            return

        with output:
            print("File hash verified!")
            print("Step 3: Verifying digital signature...")

        # Verify signature
        file_hash_bytes = hashlib.sha256(received_file['content']).digest()
        public_key_hex = public_key_input.value.strip()

        is_valid = ECCManager.verify_signature(
            file_hash_bytes,
            transaction['signature'],
            public_key_hex
        )

        if not is_valid:
            # Updated result_display.value to include text-align: center
            result_display.value = f"""
                <div style='background: #ffebee; padding: 25px; border-radius: 10px; border-left: 5px solid #f44336; border: 1px solid #ef9a9a; text-align: center;'>
                    <h3 style='color: #000000; margin-top: 0; font-weight: bold;'>Invalid Digital Signature!</h3>
                    <p style='color: #000000;'><strong>Authentication Failed:</strong> Digital signature verification failed</p>
                    <ul style='color: #000000; display: inline-block; text-align: left;'>
                        <li>The provided public key does not match the signature</li>
                        <li>Possible causes: Wrong public key or file sender is not authentic</li>
                        <li>This file cannot be verified as coming from the claimed sender</li>
                    </ul>
                    <div style='background: #fff3e0; padding: 12px; border-radius: 5px; margin-top: 15px; border: 1px solid #ffb74d;'>
                        <p style='color: #000000; margin: 0; font-weight: bold;'>Solution: Contact the sender to verify the correct public key.</p>
                    </div>
                </div>
            """
            with output:
                clear_output()
                print("Signature verification failed!")
            return

        with output:
            print("Signature verified!")
            print("All checks passed!")
            print("Downloading verified file...")

        # Download the verified file automatically
        verified_filename, drive_filename = download_verified_file(received_file['content'], received_file['name'])

        # Log successful verification
        log_activity("FILE_VERIFIED", f"File: {received_file['name']}, Sender: {transaction['sender']}, Hash: {received_hash[:16]}...")

        # Success!
        # Updated result_display.value to include text-align: center
        result_display.value = f"""
            <div style='background: #c8e6c9; padding: 25px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #4caf50; border: 1px solid #81c784; text-align: center;'>
                <h3 style='color: #000000; margin-top: 0; font-weight: bold;'>VERIFICATION SUCCESSFUL - File is AUTHENTIC!</h3>

                <div style='background: white; padding: 20px; border-radius: 8px; margin: 15px 0; border: 1px solid #c8e6c9;'>
                    <p style='color: #000000;'><strong>File Name:</strong> {received_file['name']}</p>
                    <p style='color: #000000;'><strong>Verified Sender:</strong> {transaction['sender']}</p>
                    <p style='color: #000000;'><strong>Intended Receiver:</strong> {transaction['receiver']}</p>
                    <p style='color: #000000;'><strong>File Hash (SHA-256):</strong> {received_hash[:32]}...</p>
                    <p style='color: #000000;'><strong>Transaction Time:</strong> {transaction['timestamp']}</p>
                    <p style='color: #000000;'><strong>Saved to Drive:</strong> {drive_filename}</p>
                </div>

                <div style='background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 15px 0; border: 1px solid #a5d6a7;'>
                    <p style='color: #1b5e20; margin-top: 0; font-weight: bold;'>All Security Verifications PASSED:</strong></p>
                    <ul style='color: #000000; background: white; padding: 15px; border-radius: 5px; display: inline-block; text-align: left;'>
                        <li>File exists in blockchain ledger</li>
                        <li>File integrity verified - NOT tampered</li>
                        <li>Digital signature is VALID and authentic</li>
                        <li>Sender identity confirmed</li>
                        <li>File is safe to use</li>
                        <li>File downloaded automatically</li>
                        <li>Copy saved to Google Drive</li>
                    </ul>
                </div>

                <div style='background: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 15px; border: 1px solid #64b5f6;'>
                    <p style='color: #1976d2; margin-top: 0; font-weight: bold;'>Download Status: The verified file has been automatically downloaded as <code style='background: #f5f5f5; padding: 2px 5px; border-radius: 3px;'>{verified_filename}</code></p>
                    <p style='color: #1976d2; margin-bottom: 0; font-weight: bold;'>Backup: A copy has been saved to your Google Drive at: <code style='background: #f5f5f5; padding: 2px 5px; border-radius: 3px;'>{drive_filename}</code></p>
                </div>
            </div>
        """

        with output:
            clear_output()
            print("="*70)
            print("VERIFICATION COMPLETE - FILE IS AUTHENTIC!")
            print("="*70)
            print(f"File: {received_file['name']}")
            print(f"Downloaded as: {verified_filename}")
            print(f"Saved to Drive: {drive_filename}")
            print("All security checks passed!")
            print("File is authentic and safe to use!")
            print("File download should start automatically...")

    upload_received_btn.on_click(on_upload_received_click)
    verify_btn.on_click(on_verify_click)

    # Center-align elements in the receiver UI
    centered_elements = widgets.VBox([
widgets.HTML("""
<div class='cyber-card'>
    <h2 class='glow-text' style='text-align:center;'>
        RECEIVER SIDE – Verify File Authenticity
    </h2>
    <p style='text-align:center; color:#ccc;'>
        Blockchain validation + ECC signature verification
    </p>
</div>
""")        ,
        widgets.HTML("<hr style='border: 1px solid #e0e0e0;'>"),
        widgets.HTML("""
            <div style='background: #f5f5f5; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; margin-bottom: 15px; text-align: center;'>
                <p style='color: #000000; margin: 0; font-weight: bold;'>Verification Steps:</p>
                <ol style='color: #000000; display: inline-block; text-align: left;'>
                    <li>Enter the exact file name provided by sender</li>
                    <li>Paste the sender's public key</li>
                    <li>Upload the received file</li>
                    <li>Click verify to check authenticity and auto-download</li>
                </ol>
            </div>
        """
        ),
        widgets.HBox([file_name_input], layout=widgets.Layout(justify_content='center')),
        widgets.HBox([public_key_input], layout=widgets.Layout(justify_content='center')),
        widgets.HTML("<br>"),
        widgets.HBox([upload_received_btn], layout=widgets.Layout(justify_content='center')),
        received_file_info,
        widgets.HTML("<br>"),
        widgets.HBox([verify_btn], layout=widgets.Layout(justify_content='center')),
        result_display,
        output
    ], layout=widgets.Layout(align_items='center'))
    card_start = widgets.HTML("<div class='section-card'>")
    card_title = widgets.HTML("<div class='section-title'>RECEIVER SIDE - Verify & Download</div>")
    card_end = widgets.HTML("</div>")
    
    return widgets.VBox([card_start, card_title, centered_elements, card_end])


def create_blockchain_viewer():
    """Create blockchain viewer"""

    view_btn = widgets.Button(
        description='View Blockchain Ledger',
        button_style='info',
        layout=widgets.Layout(width='220px', height='40px'),
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    refresh_btn = widgets.Button(
        description='Refresh',
        button_style='warning',
        layout=widgets.Layout(width='120px', height='40px'),
        style={'font_weight': 'bold', 'border_radius': '8px'}
    )

    blockchain_display = widgets.HTML()
    output = widgets.Output()  # Add output for status messages

    def update_blockchain_display():
        html_content = "<div style='background: #f5f5f5; padding: 25px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center;'>" # Added text-align: center
        html_content += f"<h3 style='color: #000000; text-align: center; font-weight: bold;'>Blockchain Ledger - {len(blockchain.chain)} Blocks</h3>"
        html_content += f"<p style='color: #000000; text-align: center; font-weight: bold;'>Storage Location: {BLOCKCHAIN_DIR}</p>"

        for block in blockchain.chain:
            html_content += f"""
                <div style='background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #667eea; border: 1px solid #e0e0e0;'>
                    <h4 style='color: #000000; margin-top: 0; text-align: center; font-weight: bold;'>Block #{block.index}</h4>
                    <table style='width: 100%; color: #000000; border-collapse: collapse; margin-left: auto; margin-right: auto;'>
                        <tr>
                            <td style='padding: 5px; border-bottom: 1px solid #f0f0f0;'><strong>Block Hash:</strong></td>
                            <td style='padding: 5px; border-bottom: 1px solid #f0f0f0;'><code>{block.hash[:32]}...</code></td>
                        </tr>
                        <tr>
                            <td style='padding: 5px; border-bottom: 1px solid #f0f0f0;'><strong>Previous Hash:</strong></td>
                            <td style='padding: 5px; border-bottom: 1px solid #f0f0f0;'><code>{block.previous_hash[:32]}...</code></td>
                        </tr>
                        <tr>
                            <td style='padding: 5px; border-bottom: 1px solid #f0f0f0;'><strong>Timestamp:</strong></td>
                            <td style='padding: 5px; border-bottom: 1px solid #f0f0f0;'>{block.timestamp}</td>
                        </tr>
                        <tr>
                            <td style='padding: 5px;'><strong>Nonce:</strong></td>
                            <td style='padding: 5px;'>{block.nonce}</td>
                        </tr>
                    </table>
            """

            if block.transactions:
                html_content += "<div style='margin-top: 15px;'>"
                html_content += "<strong style='color: #000000;'>Transactions:</strong>"
                html_content += "<div style='background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; border: 1px solid #e9ecef;'>"
                for tx in block.transactions:
                    html_content += f"""
                        <div style='background: white; padding: 12px; margin: 8px 0; border-radius: 5px; border-left: 3px solid #4caf50;'>
                            <strong style='color: #000000;'>{tx['file_name']}</strong><br>
                            <span style='color: #000000;'>{tx['sender']} \u2192 {tx['receiver']}</span><br>
                            <small style='color: #666;'>{tx['timestamp']}</small>
                        </div>
                    """
                html_content += "</div></div>"
            else:
                html_content += "<div style='background: #fff3e0; padding: 12px; border-radius: 5px; margin-top: 15px; border: 1px solid #ffb74d;'>"
                html_content += "<em style='color: #000000; font-weight: bold;'>Genesis Block (Initial Block)</em>"
                html_content += "</div>"

            html_content += "</div>"

        blockchain_display.value = html_content

    def on_view_click(b):
        with output:
            clear_output()
            print("Loading blockchain data...")
        update_blockchain_display()
        with output:
            clear_output()
            print("Blockchain data loaded successfully!")

    def on_refresh_click(b):
        with output:
            clear_output()
            print("Refreshing blockchain data...")
        update_blockchain_display()
        with output:
            clear_output()
            print("Blockchain data refreshed!")

    view_btn.on_click(on_view_click)
    refresh_btn.on_click(on_refresh_click)

    # Center-align elements in the blockchain viewer
    centered_elements = widgets.VBox([
widgets.HTML("""
<div class='cyber-card'>
    <h2 class='glow-text' style='text-align:center;'>
        BLOCKCHAIN EXPLORER
    </h2>
    <p style='text-align:center; color:#ccc;'>
        Immutable ledger of all secure transactions
    </p>
</div>
""")        ,
        widgets.HTML("<hr style='border: 1px solid #e0e0e0;'>"),
        widgets.HTML("<p style='color: #000000; text-align: center; font-weight: bold;'>View the complete blockchain ledger containing all file transactions.</p>"),
        widgets.HBox([view_btn, refresh_btn], layout=widgets.Layout(justify_content='center', spacing='10px')),
        output,
        widgets.HTML("<br>"),
        blockchain_display
    ], layout=widgets.Layout(align_items='center'))
    card_start = widgets.HTML("<div class='section-card'>")
    card_title = widgets.HTML("<div class='section-title'>BLOCKCHAIN EXPLORER</div>")
    card_end = widgets.HTML("</div>")
    return widgets.VBox([card_start, card_title, centered_elements, card_end])


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""

    # Create tabs
    tabs = widgets.Tab()
    tabs.children = [
        create_sender_ui(),
        create_receiver_ui(),
        create_blockchain_viewer()
    ]
    tabs.set_title(0, 'Sender')
    tabs.set_title(1, 'Receiver')
    tabs.set_title(2, 'Blockchain')

    # Display
    display(create_header())
    display(tabs)

    print("\nSecure Document Sharing System loaded successfully!")
    print("Use the tabs above to:")
    print("   1. SENDER: Upload file, generate ECC keys, and create blockchain transaction")
    print("   2. RECEIVER: Verify file authenticity using blockchain and digital signatures")
    print("   3. BLOCKCHAIN: View complete transaction ledger")
    print(f"\nGoogle Drive Integration: All data saved to {PROJECT_DIR}")
    print("\nFeatures: ECC Digital Signatures \u2022 SHA-256 Hashing \u2022 Blockchain Immutable Ledger \u2022 File Integrity Verification")
    print("Auto-Download: Verified files automatically download to your computer")
    print("Cloud Storage: All data backed up to Google Drive")


# Run the application
main()