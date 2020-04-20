from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
import requests_cache
requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36000)
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

#This GET Method obtains the capital and country record
@app.route('/eucities/<capital>', methods=['GET'])
def profile(capital):
    rows = session.execute( """Select * From eucities.stats where capital = '{}'""".format(capital))
    for eucities in rows:
        return('<h1>{} is in the country {}!</h1>'.format(capital,eucities.name))
    return jsonify({'error':'city not found'}), 404

#This DELETE Method removed record specified
@app.route('/eucities/<capital>', methods=['DELETE'])
def delete_city(capital):
    rows = session.execute( """Select * From eucities.stats where capital = '{}'""".format(capital))
    for eucities in rows:
        if eucities is None:
            return jsonify({'error':'city not found'}), 404
        else:
            rows = session.execute( """Delete From eucities.stats where capital = '{}'""".format(capital))
            return jsonify({'success': True})

#This POST Method adds a new capital city record
@app.route('/eucities/<capital>', methods=['POST'])
def post_city(capital):
    rows = session.execute( """Select * From eucities.stats where capital = '{}'""".format(capital))
    for eucities in rows:
        if eucities is None:
            return jsonify({'error':'the new city needs to have a name'}), 400
        return jsonify({'error':'this city already exists in the database'}), 400
    rows = session.execute( """Insert into eucities.stats (capital) values ('Metropolis')""")
    return jsonify({'message': 'created: /eucities/{}'.format(capital)}), 201

@app.route('/eucities/<capital>', methods=['PUT'])
def put_city(capital):
    rows = session.execute( """Select * From eucities.stats where capital = '{}'""".format(capital))
    for eucities in rows:
        if eucities is None:
            return jsonify({'error':'you cannot update a city which does not exist'}), 400
    rows = session.execute( """Update eucities.stats set name ='Genovia' where capital ='{}'""".format(capital))
    return jsonify({'message':'updated: /eucities/{}'.format(capital)}), 201

#This PUT Method adds a country to a capital city record

if __name__=="__main__":
    app.run(host='0.0.0.0', port=80)
