from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Simple Flask App by Hanif Deployed on Google App Engine!"

@app.route('/hello')
def hello():
    return render_template('index-new.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'This is some sample data',
        'numbers': [1, 2, 3, 4, 5]
    }
    return jsonify(data)

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)