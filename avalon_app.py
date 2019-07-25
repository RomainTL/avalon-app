# -*- coding: utf-8 -*-
# author: romain.121@hotmail.fr

"""This script is the RESTful web service used in Avalon"""

import argparse

from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

from avalon_pylib import avalon_blueprint


app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()
app.register_blueprint(avalon_blueprint)



# @app.route('/test_lala', methods=['GET'])
# def test_lala():
#     return jsonify({'test': 'lala'})


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    # optional arguments
    PARSER.add_argument("-host", type=str, help="app host", default='0.0.0.0')
    PARSER.add_argument("-port", type=int, help="app port", default=5000)
    PARSER.add_argument("-host_db", type=str, help="db host", default='rethinkdb')
    PARSER.add_argument("-port_db", type=int, help="db port", default=28015)

    # parse arguments
    ARGS = PARSER.parse_args()

    # Start the RESTful web service used in Avalon
    app.run(host=ARGS.host, port=ARGS.port, debug=True)
