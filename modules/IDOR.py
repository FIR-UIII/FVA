from flask import Blueprint, render_template, render_template_string


idor_bp = Blueprint("idor", __name__)

@idor_bp.route('/idor', methods=['POST', 'GET'])
def upload():
    return render_template('idor.html')

@idor_bp.route('/idor/main/', methods=['POST', 'GET'])
def idor_route():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple HTML Document</title>
        <link rel="stylesheet" href="../../static/bootstrap.min.css">
        <link rel="icon" href="../../static/scripting.png" type="image/x-icon">
    </head>
        <body>
            <div class="container mt-5">
                <h1>Welcome to simple IDOR vulnerability web app</h1>
                <p>U are user 1 </p>
                <button type="button" onclick="location.href='/idor/main/workspace1'" class="btn btn-primary">Go</button>
            </div>
            <div class="container mt-5">
                <a href="/idor" class="btn btn-secondary">Назад</a></p>
            </div>
        </body>
    </html>
    '''
    return render_template_string(html_content)

@idor_bp.route('/idor/main/workspace1', methods=['POST', 'GET'])
def idor_route_workplace():
    html_content = '''
    <html>
    <head>
        <title>Click Counter</title>
        <link rel="stylesheet" href="../../static/bootstrap.min.css">
        <link rel="icon" href="../../static/scripting.png" type="image/x-icon">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Welcome user 1 !! =)))</h1>
            <p>User 1 credentials</p>
            <p>6969 126788</p>
            <p>6969-6969-6969-8888</p>
            <h1>$8er coin</h1>
            <button id="clickButton" class="btn btn-primary">Let's go!</button>
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
        </div>
        <div class="container mt-5">
            <a href="/idor/main" class="btn btn-secondary">Назад</a></p>
        </div>        
    </body>
</html>
    '''
    return render_template_string(html_content)


@idor_bp.route('/idor/main/workspace2', methods=['POST', 'GET'])
def idor_route_workplace2():
    html_content = '''
    <html>
    <head>
        <title>Click Counter</title>
        <link rel="stylesheet" href="../../static/bootstrap.min.css">
        <link rel="icon" href="../../static/scripting.png" type="image/x-icon">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Welcome user 2 !! =)))</h1>
            <p>User 2 credentials</p>
            <p>1178 782263</p>
            <p>2318-0937-3387-2233</p>
            <h1>$8er coin</h1>
            <button id="clickButton" class="btn btn-primary">Works</button>
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
        </div>
        <div class="container mt-5">
            <a href="/idor/main" class="btn btn-secondary">Назад</a></p>
        </div>
    </body>
</html>

    '''
    return render_template_string(html_content)


