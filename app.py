from flask import Flask, request, send_file, jsonify, abort, render_template,make_response,redirect, url_for, flash
import openai
import io
import os
import jwt
import tempfile
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import datetime
# Set your Azure Speech Service credentials
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")

# Set your OpenAI API key


app = Flask(__name__)
bcrypt = Bcrypt(app)
client = MongoClient('mongodb+srv://niharmuniraju4:wfhK2TVsJiOCMgcs@goku.jrdvw1f.mongodb.net/')
db = client['GokuDB']
users_collection = db['users']
app.secret_key = 'your_secret_key_here'
  # or ('localhost.pem', 'localhost-key.pem')
@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user details from request data
        data = request.json
        username = data["username"]
        password = data["password"]
        email = data["email"]
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"error": "Username already exists!"}), 400

        # Hash password before storing in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Store user in database
        users_collection.insert_one({"password": hashed_password, "email": email})

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('reply.html')


@app.route('/converse', methods=['POST'])
def converse():
        try:
            print("hi")
            response_text = get_gpt_response(request.args.get('user_message'))
            print(response_text)
            return jsonify({"message": response_text}), 200
        # Get data from the incoming POST request
            # data = request.get_json()
            # print("hi")
            # user_message =request.args.get('user_message')

            # try:
            #     print(f"You said: {user_message}")
            #     response_text = get_gpt_response(user_message)
            #     print("ai said",response_text)
            #     return response_text
            # except Exception as e:
            #     app.logger.error("Failed to get response from GPT-3: %s", str(e))
            #     abort(500, 'Failed to get response from GPT-3.')
            # return "error 1"

        except Exception as e:

            # Handle errors and return an error response
            error_message = str(e)
            return "error 1"+error_message


def get_gpt_response(prompt):
    openai.api_key = os.getenv("OPENAI_KEY")
    prompt = f"Imagine you're an AI therapist named Goku, who loves to help people with counselling on feelings, thoughts, choices, emotions, facing fears and should make them feel good. Respond with humor to: '{prompt}'"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=80)
    # Let's add Maple's personal touch to every response
    return response.choices[0].text.strip()

@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        print(request.form.get('email') , request.form.get('password'))
        user = users_collection.find_one({'email': request.form.get('email')})
        print(user)
        if user and bcrypt.check_password_hash(user['password'], request.form.get('password')):
            return redirect('/dashboard')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
     return render_template('dashboard.html')

@app.route('/reply')
def reply():
     return render_template('reply.html')

@app.route('/home')
def home():
    return "Welcome to Home"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)