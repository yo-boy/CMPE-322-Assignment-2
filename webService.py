from flask import Flask, request
import threading
import ssl

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse():
    text = request.form['text']
    reversed_text = text[::-1]
    return reversed_text

@app.route('/fibonacci', methods=['POST'])
def fibonacci():
    position = int(request.form['position'])
    fib_number = calculate_fibonacci(position)
    return str(fib_number)

def calculate_fibonacci(n):
    a, b = 0, 1
    if n < 0:
        return "Invalid input. please enter a positive integer."
    elif n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(n-1):
            c = a + b
            a = b
            b = c
        return b

def run_http_server():
    app.run(port=80)

def run_https_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private_key.key')  # Replace with your certificate and private key paths
    app.run(port=443, ssl_context=context)

if __name__ == '__main__':
    http_thread = threading.Thread(target=run_http_server)
    https_thread = threading.Thread(target=run_https_server)

    http_thread.start()
    https_thread.start()

    http_thread.join()
    https_thread.join()
