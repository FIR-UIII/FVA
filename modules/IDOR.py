from flask import Blueprint, render_template, render_template_string, request
import psycopg2 as psql

idor_bp = Blueprint("idor", __name__)

@idor_bp.route('/idor', methods=['POST', 'GET'])
def upload():
    return render_template('idor.html')

@idor_bp.route('/idor/IDOR/', methods=['POST', 'GET'])
def idor_route():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple HTML Document</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            p {
                color: #666;
                text-align: center;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Welcmoe to simple IDOR vulnerability web app =)</h1>
        <p>U are user 1 </p>
        <button type="button" onclick="location.href='/idor/IDOR/workspace1'">Go work luser !</button>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@idor_bp.route('/idor/IDOR/workspace1', methods=['POST', 'GET'])
def idor_route_workplace():
    html_content = '''
    <html>
<head>
    <title>Click Counter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            text-align: center;
        }
        h1 {
            color: #333;
            margin-top: 50px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        p {
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Welcome user 1 !! =)))</h1>
    <p>User 1 credentials</p>
    <p>6969 126788</p>
    <p>6969-6969-6969-8888</p>
    <h1>$8er coin</h1>
    <button id="clickButton">Work,Collegi!</button>
    <p id="clickCount">0</p>

    <script>
        var clickCount = 0;
        var clickButton = document.getElementById("clickButton");
        var clickCountElement = document.getElementById("clickCount");

        clickButton.addEventListener("click", function() {
            clickCount++;
            clickCountElement.textContent = clickCount;
        });
    </script>
</body>
</html>

    '''
    return render_template_string(html_content)


@idor_bp.route('/idor/IDOR/workspace2', methods=['POST', 'GET'])
def idor_route_workplace2():
    html_content = '''
    <html>
<head>
    <title>Click Counter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            text-align: center;
        }
        h1 {
            color: #333;
            margin-top: 50px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        p {
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Welcome user 2 !! =)))</h1>
    <p>User 2 credentials</p>
    <p>1178 782263</p>
    <p>2318-0937-3387-2233</p>
    <h1>$8er coin</h1>
    <button id="clickButton">Work,Collegi!</button>
    <p id="clickCount">0</p>

    <script>
        var clickCount = 0;
        var clickButton = document.getElementById("clickButton");
        var clickCountElement = document.getElementById("clickCount");

        clickButton.addEventListener("click", function() {
            clickCount++;
            clickCountElement.textContent = clickCount;
        });
    </script>
</body>
</html>

    '''
    return render_template_string(html_content)


