from flask import Flask
from flask import request, jsonify, make_response
import json
import os
from menu import Menu

# Elastic Beanstalk looks for an 'application' that is callable by default
app = Flask(__name__)

@app.route('/shoplist', methods=['POST'])
def shoplist():
    content = request.get_json(force=True)
    dish_list = content['dish_list']
    menu = Menu(dish_list)
    shop_list = menu.get_list()
    print(shop_list)
    return shop_list

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return "ok"

# Run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    app.debug = True
    app.run(host="0.0.0.0", debug=True)