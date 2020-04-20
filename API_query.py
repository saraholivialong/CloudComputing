from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
import requests_cache

requests_cache.install_cache('cities_api_cache', backend='sqlite', expire_after=36000)

app = Flask(__name__)
url = "https://restcountries.eu/rest/v2/region/europe"
@app.route('/cities', methods=['GET'])
def citydata():
    resp = requests.request("GET", url)
    if resp.ok:
        return jsonify(resp.json())
    else:
        print(resp.reason)

if __name__=="__main__":
    app.run(host='0.0.0.0')
