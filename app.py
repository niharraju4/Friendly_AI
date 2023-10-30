from flask import Flask, request, send_file, jsonify, abort, render_template,make_response,redirect, url_for, flash,Response
import openai
import io
import os
import jwt
import tempfile
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import datetime
from datetime import datetime,timedelta



# Set your Azure Speech Service credentials
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")

# Set your OpenAI API key


app = Flask(__name__)


bcrypt = Bcrypt(app)
client = MongoClient('mongodb+srv://niharmuniraju4:wfhK2TVsJiOCMgcs@goku.jrdvw1f.mongodb.net/')
db = client['GokuDB']
users_collection = db['users']
conversations_collection = db['session']
app.secret_key = 'your_secret_key_here'
  # or ('localhost.pem', 'localhost-key.pem')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get user details from request data
        data = request.json
        name = data["username"]
        password = data["password"]
        email = data["email"]
        print(email)
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"error": "Username already exists!"}), 400

        # Hash password before storing in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Store user in database
        users_collection.insert_one({"password": hashed_password, "email": email,"UserName":name})
        return jsonify({"message": "Data received"}), 200
    return render_template('signup.html') 

# Set Referrer-Policy header for all responses
@app.after_request
def set_referrer_policy(response):
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.before_request
def verify_jwt():
    print(request.endpoint)
    if request.endpoint == 'signin':
        return  # Skip JWT verification for login route
    if request.endpoint == 'signup':
        return  # Skip JWT verification for login route
    if request.endpoint is None:
        return  # Skip JWT verification for login route
    token = request.cookies.get('token')
    if not token:
        return "Missing token", 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
    except jwt.ExpiredSignatureError:
        return render_template('website.html')
    except jwt.InvalidTokenError:
        return "Invalid token", 401


@app.route('/chat', methods=['GET'])
def chat():
    return render_template('reply.html')


@app.route('/converse1', methods=['POST','OPTIONS'])
def converse1():
    try:
        prompt01 = os.getenv("PROMPT01")
        token = request.cookies.get('token')
        question = request.args.get('user_message')
        messages=[
            {"role": "system", "content": prompt01}
            ]
        
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data['user']
        print(f"Decoded email: {email}") # Debugging

        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=20)
        query = {
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            },
            "email": email
        }
        print(f"Query: {query}") # Debugging

        results = conversations_collection.find(query)
        if(results):
            for result in results: # Adjust the range as needed
                
                messages.append({"role": "user", "content": result.get('questions', 'N/A')})

                # Simulate the assistant's response (you might replace this with actual logic)
                messages.append({"role": "assistant", "content": result.get('response', 'N/A')})
        messages.append({"role": "user", "content": question})
        response_text = get_gpt_response1(messages)
        # Current date and time
        record = {
            'email':email,
            'questions': question,
            'response': response_text,
            'timestamp': datetime.now()
        }
        conversations_collection.insert_one(record)
            
        response = polly_client.synthesize_speech(
            VoiceId='Joanna',  # You can change the voice ID as needed
            OutputFormat='mp3',
            Text=response_text
        )

        return Response(
            response['AudioStream'].read(),
            content_type='audio/mp3'
        )
        # return jsonify({"message": response_text}), 200

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        return "error 1"+error_message

@app.route('/converse2', methods=['POST'])
def converse2():
    try:
        prompt02 = os.getenv("PROMPT02")
        token = request.cookies.get('token')
        question = request.args.get('user_message')
        messages=[
            {"role": "system", "content": prompt02}
            ]
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=20)
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data['user']
        query = {
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            },
            "email": email
        }
        results = conversations_collection.find(query)
        if(results):
            for result in results: # Adjust the range as needed
                
                messages.append({"role": "user", "content": result.get('questions', 'N/A')})

                # Simulate the assistant's response (you might replace this with actual logic)
                messages.append({"role": "assistant", "content": result.get('response', 'N/A')})
        messages.append({"role": "user", "content": question})
        response_text = get_gpt_response2(messages)
        # Current date and time
        record = {
            'email':email,
            'questions': question,
            'response': response_text,
            'timestamp': datetime.now()
        }
        conversations_collection.insert_one(record)
        return jsonify({"message": response_text}), 200

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        return "error 1"+error_message

@app.route('/converse3', methods=['POST'])
def converse3():

    try:
        prompt03 = os.getenv("PROMPT03")
        token = request.cookies.get('token')
        question = request.args.get('user_message')
        messages=[
            {"role": "system", "content": prompt03}
            ]
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=20)
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data['user']
        query = {
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            },
            "email": email
        }
        results = conversations_collection.find(query)
        if(results):
            for result in results: # Adjust the range as needed
                
                messages.append({"role": "user", "content": result.get('questions', 'N/A')})

                # Simulate the assistant's response (you might replace this with actual logic)
                messages.append({"role": "assistant", "content": result.get('response', 'N/A')})
        messages.append({"role": "user", "content": question})
        response_text = get_gpt_response3(messages)
        # Current date and time
        record = {
            'email':email,
            'questions': question,
            'response': response_text,
            'timestamp': datetime.now()
        }
        conversations_collection.insert_one(record)
        return jsonify({"message": response_text}), 200

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        return "error 1"+error_message
        
def get_gpt_response1(prompt):
    openai.api_key = os.getenv("OPENAI_KEY")
    print("hi",prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    print(response)
    # Let's add Maple's personal touch to every response
    return response['choices'][0]['message']['content'].strip()
        
def get_gpt_response2(prompt):
    openai.api_key = os.getenv("OPENAI_KEY")
    prompt = f"Imagine you're an AI therapist, who loves to help people with counselling on thought Patterns, Emotional Regulation, Decision-Making, Mood Swings, Facing Fears, Relationships, Self-Esteem, Sleep Issues, Sexuality and Identity, Goal Setting, Academic Stress, Mindfulness, Career Choices, Eating Habits, Breakups, Digital Wellbeing, Imposter Syndrome, Pet Loss, Global Concerns, Communication Skills, Physical Health, Financial Stress, Parenting, Addictions, Grief, loss and you should make them feel good by the end of each converstation. Respond with humor to: '{prompt}'"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=80)
    # Let's add Maple's personal touch to every response
    return response.choices[0].text.strip()
def get_gpt_response3(prompt):
    openai.api_key = os.getenv("OPENAI_KEY")
    prompt = f"Imagine you're an AI therapist, who loves to help people with counselling on thought Patterns, Emotional Regulation, Decision-Making, Mood Swings, Facing Fears, Relationships, Self-Esteem, Sleep Issues, Sexuality and Identity, Goal Setting, Academic Stress, Mindfulness, Career Choices, Eating Habits, Breakups, Digital Wellbeing, Imposter Syndrome, Pet Loss, Global Concerns, Communication Skills, Physical Health, Financial Stress, Parenting, Addictions, Grief, loss and you should make them feel good by the end of each converstation. Respond with humor to: '{prompt}'"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=80)
    # Let's add Maple's personal touch to every response
    return response.choices[0].text.strip()

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        print(request.form.get('email') , request.form.get('password'))
        user = users_collection.find_one({'email': request.form.get('email')})
        
        if user and bcrypt.check_password_hash(user['password'], request.form.get('password')):
            token = jwt.encode({
            'user': user['email'],
            'exp': datetime.utcnow() + timedelta(minutes=20)
        }, app.config['SECRET_KEY'])

            resp = make_response(redirect('dashboard'))
            resp.set_cookie('token', token)
            return resp
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

@app.route('/')
def website():
    print('hi')
    return render_template('website.html')

@app.route('/reply1')
def reply1():
     return render_template('reply1.html')


@app.route('/reply2')
def reply2():
     return render_template('reply2.html')

@app.route('/reply3')
def reply3():
     return render_template('reply3.html')
@app.route('/home')
def home():
    return "Welcome to Home"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

@app.route('/logout', methods=['POST'])
def logout():
    # Add your session termination logic here, if needed ,ssl_context=("cert.pem","key.pem")
    return jsonify({'status': 'success'})
