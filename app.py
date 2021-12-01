from flask import *
from cpu_stress import stress
from scraper import get_data
import tasks

app = Flask(__name__)

@app.route('/ping',methods=['GET'])
def ping():

    return jsonify({"ping":"pong"})

@app.route('/crawl',methods=['GET'])
def crawl():

    tasks.crawl.delay()

    return jsonify({"Message":"Task Started"})

if __name__ == '__main__':

	app.run(host='0.0.0.0', port=8080, debug=True)
