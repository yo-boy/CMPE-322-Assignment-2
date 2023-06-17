# import all the required libraries and request module from flask
from flask import Flask, request
import requests
import ssl
import threading

# create the required flask application
app = Flask(__name__)

# setting the server url to be used with http 
serverURL = 'http://localhost:80'

# defining the simple html for each of our pages
# the index, the reverse string page, and the fibonacci page
indexHTML =  '''
    <a href="/reverse">Reverse a String</a>
    <br>
    <a href="/fibonacci">Calculate Fibonacci Number</a>
    '''
reverseHTML = '''
    <form method="POST" action="/reverse">
        <input type="text" name="text" />
        <input type="submit" value="Reverse" />
    </form>
    '''
fibonacciHTML = '''
    <form method="POST" action="/fibonacci">
        <input type="number" name="index" />
        <input type="submit" value="Calculate" />
    </form>
    '''

# route decorator for the root url of the server
@app.route('/')
def home():
    return indexHTML

# route decorator for the reverse string url
@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    # check if the request is post or get, we supply the html page if it's a get request
    # if it's a post request we get the response from the webService and return it
    if request.method == 'POST':
        text = request.form['text']
        response = sendRequest(serverURL, '/reverse', {'text': text})
        return f'Reversed text: {response}'
    return reverseHTML

# route decorator for the fibonacci page
@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    # check if the request is get or post, supply the html page if it's a get request
    # if it's a post request we get the response from the webService and display it
    if request.method == 'POST':
        index = int(request.form['index'])
        response = sendRequest(serverURL, '/fibonacci', {'index': index})
        return f'Fibonacci number at position {index}: {response}'
    return fibonacciHTML

# function that takes the server url the REST endpoint and the data to send a request
def sendRequest(baseURL, endpoint, data):
    # first the full url is constructed
    url = f'{baseURL}{endpoint}'
    # then the request is made and the response is returned
    response = requests.post(url, data=data, verify=False)
    return response.text

# function made to run an http server on port 900
def runHttpServer():
    # Run the HTTP server on port 900
    app.run(port=900)

# function made to run an https server on port 901
def runHttpsServer():
    # first we configure serverURL so we talk to the webService using https too
    serverURL = 'https://localhost:443'
    # setup the ssl encryption to be able to enable https using a self signed cert
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private_key.key')
    # Run the HTTPS server on port 901
    app.run(port=901, ssl_context=context)

# main function
def main():
    # create two threads to run the http and https servers
    httpThread = threading.Thread(target=runHttpServer)
    httpsThread = threading.Thread(target=runHttpsServer)
    # start the two servers
    httpThread.start()
    httpsThread.start()
    # wait for the servers to exit
    httpThread.join()
    httpsThread.join()

    
# only run the webserver if the code is executed as a script
if __name__ == '__main__':
    main()
