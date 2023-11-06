from flask import Flask
from flask import render_template
from flask import Flask, request, jsonify
#import requests

app = Flask(__name__)

def InterCom():
   # Signal = requests.from[""]
    pass
@app.route('/', methods=['POST'])
def recieve_signal():
    global Signal
    data = request.get_json()
    Signal = data.get('SignalVal')

    print('data recived: ', Signal)
    return jsonify({"response": "Tag Hit"})
    
@app.route('/')
def StartSite():
    TestVal = Signal
    return render_template("OrderScreenTest.html",Signal=TestVal )
    

#if __name__ == "__main__":
   # app.run()

    #why the app.run() though'
app.run()