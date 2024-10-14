from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px

app = Flask(__name__)

# Load data
data = pd.read_csv('D:\TubsAMY\Modul Kuliah\SEMESTER 7\Sistem Penunjang Keputusan\Tugas SPK\Tugas1\Sistem_Penunjang_Keputusan-Decision_Support_System\Top 100 Crypto\Dataset\Dataset\crypto_data_coinmarketcap.csv')

# Select criteria for analysis
criteria = ['current_price', 'price_change_percentage_24h', 'market_cap', 'total_volume']

def normalize(column, weight, is_benefit=True):
    if is_benefit:
        return weight * (column - column.min()) / (column.max() - column.min())
    else:
        return weight * (column.max() - column) / (column.max() - column.min())

def apply_saw(data, criteria, weights):
    normalized_data = pd.DataFrame()
    
    for criterion in criteria:
        if criterion in ['current_price', 'market_cap', 'total_volume']:
            normalized_data[criterion] = normalize(data[criterion], weights[criterion])
        else:
            normalized_data[criterion] = normalize(data[criterion], weights[criterion])
    
    data['saw_score'] = normalized_data.sum(axis=1)
    return data.sort_values('saw_score', ascending=False)

@app.route('/')
def index():
    return render_template('index.html', criteria=criteria)

@app.route('/analyze', methods=['POST'])
def analyze():
    weights = {criterion: float(request.form[criterion]) for criterion in criteria}
    result = apply_saw(data, criteria, weights)
    top_10 = result[['name', 'saw_score'] + criteria].head(10).to_dict('records')
    
    fig = px.bar(result.head(10), x='name', y='saw_score', title='Top 10 Cryptocurrencies based on SAW Method')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({'top_10': top_10, 'graph': graph_json})

if __name__ == '__main__':
    app.run(debug=True)
