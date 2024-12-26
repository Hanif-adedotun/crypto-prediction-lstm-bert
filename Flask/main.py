from flask import Flask, request, jsonify, render_template
import io
import base64
import pandas as pd 
import os
import joblib
import numpy as np
import keras
from sklearn.preprocessing import StandardScaler  # Add this import
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

def convert_date_format(date_str):
    date_list = date_str.split('/')
    return f"{date_list[2]}-{date_list[1]}-{date_list[0]}"

def predict_prices(x, model, scale):
     predictions = model.predict(x)
     predictions = scale.inverse_transform(predictions.reshape(-1,1)).reshape(-1,1)
     return predictions
 
def plot_graph(predictions, real, xticks_bar):
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(predictions, marker="+", color = "green")

    plt.xlabel("Date range", fontsize = 10, labelpad = 10)
    ax.set_xticks(range(len(xticks_bar)))
    ax.set_xticklabels(xticks_bar, rotation=45, ha='right')
    
    plt.ylabel("Price in USD", fontsize = 10, labelpad = 20)
    plt.title("LSTM_BERT Prediction", fontsize = 20, pad = 20)
    plt.savefig('./static/new_plot.png')

    
def run_model(startdate, enddate):   
    print(startdate, enddate)         
    df = pd.read_csv("./data/BERT_sentiment_withprices.csv")
    price_model = keras.models.load_model('./data/price_model_v1.keras')
    test_scaler = joblib.load("./data/scaler.pkl")
    
    stock_column = ['prices']
    news_column = ['sentiment']
    
    start_date = df.index[df["date"] == startdate].tolist()
    end_date = df.index[df["date"] == enddate].tolist()
    
    if len(start_date) == 0 or len(end_date) == 0:
        return "Sentiment data not available"
    
    if start_date[0] < 11:
        return "Sentiment data not available"
    
    curr_date = start_date[0]  
    length = end_date[0]-start_date[0]
    
    predictions = []
    real =[]
    
    for i in range(length):
        prices = df.get(stock_column).values[curr_date-10:curr_date]
        y_price =  df.get(stock_column).values[curr_date]
        prices_sentiment = df.get(news_column).values[curr_date-10:curr_date]
        
        prices = test_scaler.transform(prices)
        
        real.append(y_price[0])
        
        # splitting testing data to x and y
        X_prices = [prices[0 : 10]]
        
        X_prices[0] = X_prices[0].tolist()
        X_prices[0].append(prices_sentiment[-1].tolist())
        X_prices = np.array(X_prices).astype(float)
        price_prediction = predict_prices(X_prices, price_model, test_scaler)
        predictions.append(price_prediction[0][0])
        
        curr_date += 1
        
    # print(prices, y_price, prices_sentiment)
    xticks_bar = df.loc[start_date[0]:end_date[0], "date"].tolist()
    plot_graph(predictions, real, xticks_bar)
    print(predictions)
    print(real)
    return predictions, xticks_bar
    
    
@app.route('/')
def home():
    return render_template('index-new.html') 

@app.route('/submit', methods=['POST'])
def get_data():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    days = request.form['days']
    print("Days", days)
    predictions, x_bars = run_model(convert_date_format(startDate), convert_date_format(endDate))
    
    # "https://github.com/user-attachments/assets/e03291f8-1252-4e92-9cb6-45abc1104b64"
    return render_template('result-new.html', 
                           price = predictions,
                           len=len(predictions),
                           days = x_bars,
                           plot_url = '/static/new_plot.png') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)