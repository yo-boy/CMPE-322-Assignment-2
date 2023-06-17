from flask import Flask, request
import requests
import ssl
import threading

app = Flask(__name__)

serverURL = 'http://localhost:80'

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

@app.route('/')
def home():
    return indexHTML

@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    if request.method == 'POST':
        text = request.form['text']
        response = sendRequest(serverURL, '/reverse', {'text': text})
        return f'Reversed text: {response}'
    return reverseHTML

@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    if request.method == 'POST':
        index = int(request.form['index'])
        response = sendRequest(serverURL, '/fibonacci', {'index': index})
        return f'Fibonacci number at position {index}: {response}'
    return fibonacciHTML
    
def sendRequest(baseURL, endpoint, data):
    url = f'{baseURL}{endpoint}'
    response = requests.post(url, data=data, verify=False)
    return response.text
    
def runHttpServer():
    # Run the HTTP server on port 900
    app.run(port=900)

def runHttpsServer():
    serverURL = 'https://localhost:443'
    # Run the HTTPS server on port 901
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private_key.key')  # Replace with your certificate and private key paths
    app.run(port=901, ssl_context=context)

if __name__ == '__main__':
    httpThread = threading.Thread(target=runHttpServer)
    httpsThread = threading.Thread(target=runHttpsServer)

    httpThread.start()
    httpsThread.start()

    httpThread.join()
    httpsThread.join()
