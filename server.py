from flask import Flask, jsonify, request
from waitress import serve

from error import InvalidUsage
from s1query import get_query

app = Flask(__name__)


def has_args(iterable, args):
    """Verify that all args are in the iterable."""

    try:
        return all(x in iterable for x in args)

    except TypeError:
        return False


@app.route('/', methods=['GET'])
def ping():
    return 'success'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/getS1file', methods=['GET'])
def get_s1_file():
    if not has_args(request.json, ['ticker']):
        raise InvalidUsage('Missing ticker parameter')
    ticker = request.json['ticker']
    assert type(ticker) == str
    
    
    
    
    get_link = get_query(ticker)
    
    results = {}
    for filings in output:
        txt_link = filings['linkToTxt']
        if filings["formType"] == "S-1":
            key_string = filings['formType'] + " " + filings['filedAt']
            results[key_string] = txt_link

    return jsonify(results)

serve(app, host='0.0.0.0', port=3000, threads=10)
