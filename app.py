from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "UGH28Bkpoy9RaLQLX7dy2KWSnuavUwPSWVvBtW2ml1s="  

guest_tokens = {}

@app.route('/request_access', methods=['POST'])
def request_access():
    data = request.json
    guest_name = data.get('name')
    duration_hours = int(data.get('duration', 24))
    
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=duration_hours)
    token = jwt.encode({
        'guest_name': guest_name,
        'exp': expiration_time
    }, SECRET_KEY, algorithm='HS256')
    
    guest_tokens[token] = {
        'name': guest_name,
        'expires': expiration_time
    }
    
    access_link = f"http://yourdomain.com/guest_access/{token}"
    return jsonify({"link": access_link})

@app.route('/guest_access/<token>', methods=['GET'])
def guest_access(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return f"Hello {data['guest_name']}! Your access is valid until {data['exp']}."
    except jwt.ExpiredSignatureError:
        return "Access expired."
    except jwt.InvalidTokenError:
        return "Invalid access token."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

