from flask import Flask, request
import threading
import ssl

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse():
    text = request.form['text']
    reversedText = text[::-1]
    return reversedText

@app.route('/fibonacci', methods=['POST'])
def fibonacci():
    position = int(request.form['index'])
    fibNumber = calculateFibonacci(position)
    return str(fibNumber)

def calculateFibonacci(n):
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

def runHttpServer():
    app.run(port=80)

def runHttpsServer():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private_key.key')  # Replace with your certificate and private key paths
    app.run(port=443, ssl_context=context)

if __name__ == '__main__':
    httpThread = threading.Thread(target=runHttpServer)
    httpsThread = threading.Thread(target=runHttpsServer)

    httpThread.start()
    httpsThread.start()

    httpThread.join()
    httpsThread.join()
