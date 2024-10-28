from flask import Flask, request, jsonify, render_template
import io
import base64
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Simple Flask App by Hanif Deployed on Google App Engine!"

@app.route('/hello')
def hello():
    return render_template('index-new.html')

@app.route('/graph')
def show_graph():
     return render_template('index-new.html', plot_url = "https://github.com/user-attachments/assets/e03291f8-1252-4e92-9cb6-45abc1104b64") 

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
    # request.form['']
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)