# from flask import Flask, render_template, request, send_file, jsonify
# import requests  # Import requests for OpenAI API interaction
# from werkzeug.utils import secure_filename
# import os
# from modules.encoding_module import encode_text_in_image
# from modules.decoding_module import decode_image_to_text

# app = Flask(__name__, static_folder='static')
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['ENCODED_IMAGES'] = 'static/encoded'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/encode', methods=['GET', 'POST'])
# def encode():
#     if request.method == 'POST':
#         file = request.files['inputImage']
#         text = request.form['inputText']
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # Call your encoding function here
#             encoded_image_name = encode_text_in_image(file_path, text, app.config['ENCODED_IMAGES'])
#             return jsonify({'encodedImagePath': encoded_image_name})
#             # print(encoded_image_path)
#             # return send_file(encoded_image_path, mimetype='image/png')
#     return render_template('encode.html')


# @app.route('/decode', methods=['GET','POST'])
# def decode():  
#     if request.method == 'POST':  
#         file = request.files['inputImage']  
#         if file:  
#             filename = secure_filename(file.filename)  
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
#             file.save(file_path)  
#             # Call your decoding function which should return the decoded text  
#             decoded_text = decode_image_to_text(file_path)  

#             return jsonify({'decodedText': decoded_text})
#     if request.method == 'POST':
#         file = request.files['inputImage']
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
#             # Call your decoding function which should return the decoded text
#             decoded_text = decode_image_to_text(file_path)
#             return jsonify({'decodedText': decoded_text})
#     return render_template('decode.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# from flask import Flask, render_template, request, send_file, jsonify
# import requests  # Import requests for OpenAI API interaction
# from werkzeug.utils import secure_filename
# import os
# from modules.encoding_module import encode_text_in_image
# from modules.decoding_module import decode_image_to_text

# app = Flask(__name__, static_folder='static')
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['ENCODED_IMAGES'] = 'static/encoded'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/encode', methods=['GET', 'POST'])
# def encode():
#     if request.method == 'POST':
#         file = request.files['inputImage']
#         text = request.form['inputText']
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # Call your encoding function here
#             encoded_image_name = encode_text_in_image(file_path, text, app.config['ENCODED_IMAGES'])
#             return jsonify({'encodedImagePath': encoded_image_name})
#             # print(encoded_image_path)
#             # return send_file(encoded_image_path, mimetype='image/png')
#     return render_template('encode.html')


# @app.route('/decode', methods=['GET','POST'])
# def decode():  
#     if request.method == 'POST':  
#         file = request.files['inputImage']  
#         if file:  
#             filename = secure_filename(file.filename)  
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
#             file.save(file_path)  
#             # Call your decoding function which should return the decoded text  
#             decoded_text = decode_image_to_text(file_path)  

#             return jsonify({'decodedText': decoded_text})
#     if request.method == 'POST':
#         file = request.files['inputImage']
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
#             # Call your decoding function which should return the decoded text
#             decoded_text = decode_image_to_text(file_path)
#             return jsonify({'decodedText': decoded_text})
#     return render_template('decode.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



from flask import Flask, render_template, request, jsonify
import os
import hashlib
from werkzeug.utils import secure_filename
from modules.encoding_module import encode_text_in_image
from modules.decoding_module import decode_image_to_text
from web3 import Web3

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["ENCODED_IMAGES"] = "static/encoded"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["ENCODED_IMAGES"], exist_ok=True)

# ✅ Web3 and Smart Contract Setup
INFURA_URL = "https://sepolia.infura.io/v3/43232e6c63fd40fdba6a09c8c89cf964"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not web3.is_connected():
    raise Exception("❌ Failed to connect to Sepolia Ethereum network")

CONTRACT_ADDRESS = "0xe188cc7eb0e5792cebe0d37aa8956ed49012b294"
ABI = [
    {
        "inputs": [{"internalType": "string", "name": "imageId", "type": "string"},
                   {"internalType": "string", "name": "hash", "type": "string"}],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "imageId", "type": "string"}],
        "name": "getHash",
        "outputs": [{"internalType": "string", "name": "", "type": "string"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                    {"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]
#contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS), 
    abi=ABI
)


PRIVATE_KEY = "6cc72c1212e73a7f6175e4167b733541bdaf028889ead6acce0d873b2c74880b"  # ⚠️ Replace with your real private key
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

def hash_text(text):
    """Hash extracted text using SHA-256."""
    return hashlib.sha256(text.encode()).hexdigest()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        file = request.files.get('inputImage')
        text = request.form.get('inputText')

        if not file or not text:
            return jsonify({'error': 'Missing image or text'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            encoded_image_name = encode_text_in_image(file_path, text, app.config['ENCODED_IMAGES'])
            encoded_image_path = f"/static/encoded/{encoded_image_name}"  # Correct URL path

            # If it's an API request, return JSON
            if request.headers.get('Accept') == 'application/json':
                return jsonify({'encodedImagePath': encoded_image_path})

            # Otherwise, render the HTML page with the image preview
            return render_template('encode.html', encodedImagePath=encoded_image_path, encodedImageName=encoded_image_name)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('encode.html')


@app.route("/decode", methods=["GET", "POST"])
def decode():
    if request.method == "POST":
        if "inputImage" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["inputImage"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        try:
            decoded_text = decode_image_to_text(file_path)
            return jsonify({"decodedText": decoded_text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template("decode.html")
@app.route("/store_hash", methods=["GET"])
def store_hash_form():
    return render_template("store_hash.html")  # Renders an HTML form

@app.route("/store_hash_submit", methods=["POST"])
def store_hash():
    file = request.files.get("inputImage")
    text = request.form.get("inputText")

    if not file or not text:
        return jsonify({"error": "Missing image or text"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        # Generate SHA-256 hash of the uploaded image
        with open(file_path, "rb") as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()

        # Store the hash and text on the blockchain
        txn = contract.functions.storeHash(image_hash, text).build_transaction({
            "chainId": 11155111,  # Sepolia Testnet Chain ID
            "gas": 200000,
            "gasPrice": web3.to_wei("10", "gwei"),
            "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS),
        })

        # Sign and send the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        # txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)


        return jsonify({
            "message": "Image hash stored successfully",
            "imageHash": image_hash,
            "transactionHash": txn_hash.hex()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/retrieve_hash", methods=["GET"])
def retrieve_hash_form():
    return render_template("retrieve_hash.html")  # Renders an HTML form

@app.route("/retrieve_hash_submit", methods=["POST"])
def retrieve_hash():
    file = request.files.get("inputImage")

    if not file:
        return jsonify({"error": "No image provided"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        # Compute SHA-256 hash of uploaded image
        with open(file_path, "rb") as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()

        # Retrieve stored text from blockchain
        # stored_secret = contract.functions.retrieveHash(image_hash).call()
        stored_secret = contract.functions.getHash(image_hash).call()


        if stored_secret:
            return jsonify({
                "message": "Image hash found on blockchain",
                "decodedText": stored_secret
            })
        else:
            return jsonify({
                "message": "No matching record found",
                "decodedText": None
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
