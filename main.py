from flask import Flask, redirect, url_for, render_template, request
from hashlib import md5
from Crypto.Cipher import DES3

app = Flask(__name__,template_folder='Templates')

@app.route('/')
def welcome():
    return render_template('index.html')


### Result checker submit html page
@app.route('/submit', methods=['POST', 'GET'])
def submit(operation=None):
    total_score = 0
    if request.method == 'POST':
        choice = (request.form['choose'])
        key = (request.form['id'])
        file_path = (request.form['filePath'])

        key_hash = md5(key.encode('ascii')).digest()
        # Adjust key parity of generated Hash Key for Final Triple DES Key
        tdes_key = DES3.adjust_key_parity(key_hash)

        #  Cipher with integration of Triple DES key, MODE_EAX for Confidentiality & Authentication
        #  and nonce for generating random / pseudo random number
        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

        # Open & read file from given path
        with open(file_path, 'rb') as input_file:
            file_bytes = input_file.read()

            if operation == '1':
                # Perform Encryption operation
                new_file_bytes = cipher.encrypt(file_bytes)
                
            else:
                # Perform Decryption operation
                new_file_bytes = cipher.decrypt(file_bytes)

        # Write updated values in file from given path
        with open(file_path, 'wb') as output_file:
            output_file.write(new_file_bytes)
            print('Operation Done!')

    return "Success"


if __name__ == '__main__':
    app.run(debug=True)
