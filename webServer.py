from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <a href="/reverse">Reverse a String</a>
    <br>
    <a href="/fibonacci">Calculate Fibonacci Number</a>
    '''

@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    if request.method == 'POST':
        text = request.form['text']
        reversed_text = text[::-1]
        return f'Reversed text: {reversed_text}'
    return '''
    <form method="POST" action="/reverse">
        <input type="text" name="text" />
        <input type="submit" value="Reverse" />
    </form>
    '''

@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    if request.method == 'POST':
        position = int(request.form['position'])
        fib_number = calculate_fibonacci(position)
        return f'Fibonacci number at position {position}: {fib_number}'
    return '''
    <form method="POST" action="/fibonacci">
        <input type="number" name="position" />
        <input type="submit" value="Calculate" />
    </form>
    '''

def calculate_fibonacci(n):
    if n <= 0:
        return "Invalid input. Please enter a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        return b

if __name__ == '__main__':
    app.run()
