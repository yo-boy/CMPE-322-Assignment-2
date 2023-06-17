from flask import Flask, request
import requests
import ssl
import threading

app = Flask(__name__)

SERVER_URL = 'http://localhost:80'

index_html =  '''
    <a href="/reverse">Reverse a String</a>
    <br>
    <a href="/fibonacci">Calculate Fibonacci Number</a>
    '''
reverse_html = '''
    <form method="POST" action="/reverse">
        <input type="text" name="text" />
        <input type="submit" value="Reverse" />
    </form>
    '''
fibonacci_html = '''
    <form method="POST" action="/fibonacci">
        <input type="number" name="position" />
        <input type="submit" value="Calculate" />
    </form>
    '''

@app.route('/')
def home():
    return index_html

@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    if request.method == 'POST':
        text = request.form['text']
        response = send_request(SERVER_URL, '/reverse', {'text': text})
        return f'Reversed text: {response}'
    return reverse_html

@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    if request.method == 'POST':
        position = int(request.form['position'])
        response = send_request(SERVER_URL, '/fibonacci', {'position': position})
        return f'Fibonacci number at position {position}: {response}'
    return fibonacci_html
    
def send_request(base_url, endpoint, data):
    url = f'{base_url}{endpoint}'
    response = requests.post(url, data=data, verify=False)
    return response.text
    
def run_http_server():
    # Run the HTTP server on port 900
    app.run(port=900)

def run_https_server():
    SERVER_URL = 'https://localhost:443'
    # Run the HTTPS server on port 901
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private_key.key')  # Replace with your certificate and private key paths
    app.run(port=901, ssl_context=context)

if __name__ == '__main__':
    http_thread = threading.Thread(target=run_http_server)
    https_thread = threading.Thread(target=run_https_server)

    http_thread.start()
    https_thread.start()

    http_thread.join()
    https_thread.join()
