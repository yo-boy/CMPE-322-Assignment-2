# import flask and threading and ssl (for https)
from flask import Flask, request
import threading
import ssl

# creating the flask app
app = Flask(__name__)

# route decorator for the reverse url endpoint
@app.route('/reverse', methods=['POST'])
def reverse():
    # we take the text from the request and flip it using a list operator
    text = request.form['text']
    reversedText = text[::-1]
    return reversedText

# route decorator for the fibonacci endpoint
@app.route('/fibonacci', methods=['POST'])
def fibonacci():
    # take the index from the request and calculate the fibonacci number
    position = int(request.form['index'])
    fibNumber = calculateFibonacci(position)
    # we cast it to string since that is the expected output
    return str(fibNumber)

# function to calculate the fibonacci number at index n
def calculateFibonacci(n):
    if n > 20577:
        return "Invalid input. number is too large, please enter a smaller one. (limit is 20577)"
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

# function to run the http server on port 80
def runHttpServer():
    app.run(port=80)

# function to run the https server on port 443
def runHttpsServer():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private_key.key')
    app.run(port=443, ssl_context=context)

# main function
def main():
    # create two threads to run the http and https servers
    httpThread = threading.Thread(target=runHttpServer)
    httpsThread = threading.Thread(target=runHttpsServer)
    # start both server threads
    httpThread.start()
    httpsThread.start()
    # wait for both servers to exit
    httpThread.join()
    httpsThread.join()

# only run the server threads if the code is executed as a script
if __name__ == '__main__':
    main()
