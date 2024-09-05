from flask import Flask, render_template, Blueprint
from flask_sock import Sock

csrf_bp = Blueprint('chat', __name__)

app = Flask(__name__)
sock = Sock(app)


@app.route('/chat')
def index():
    return '''<!doctype html>
<html>
  <head>
    <title>Flask-Sock Demo</title>
  </head>
  <body>
    <h1>Flask-Sock Demo</h1>
    <div id="log"></div>
    <br>
    <form id="form">
      <label for="text">Input: </label>
      <input type="text" id="text" autofocus>
    </form>
    <script>
      const log = (text, color) => {
        document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
      };

      const socket = new WebSocket('ws://' + location.host + '/echo');
      socket.addEventListener('message', ev => {
        log('<<< ' + ev.data, 'blue');
      });
      document.getElementById('form').onsubmit = ev => {
        ev.preventDefault();
        const textField = document.getElementById('text');
        log('>>> ' + textField.value, 'red');
        socket.send(textField.value);
        textField.value = '';
      };
    </script>
  </body>
</html>'''


@sock.route('/echo')
def echo(sock):
    '''получает ответ от клиента и отправялет его данные с'''
    while True:
        data = sock.receive()
        data = 'server answer '+data
        print(data) 
        sock.send(data)

if __name__ == '__main__':
    app.run(debug=True)
