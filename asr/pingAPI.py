from flask import Flask

app = Flask(__name__)  #create flask application

@app.route('/ping', methods=['GET'])  #route definition that accepts GET requests
def ping():  # a function that returns a string 'pong' when 'ping' endpoint is accessed
    return 'pong'

if __name__ == '__main__':  #only runs when script is executed directly
    app.run(debug=True, port=8001)  #run the application on port 8001 with debugging enabled
