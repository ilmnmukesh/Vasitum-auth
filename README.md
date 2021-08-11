
# VASITUM

### Install packages
##### Using this command to install packages
` pip install -r requirements.txt  `

### Setup 
##### Create .env, add
```
set EMAIL_HOST_USER=host_mail
set EMAIL_HOST_PASSWORD=host_password
```
### Runserver, continue as django


### **Documentations for login/signup using with/without gmail**

### 1. Normal Register:

##### &emsp;&emsp;METHOD: POST

##### &emsp;&emsp;HEADERS:

##### &emsp;&emsp;&emsp;&emsp;Authorization: Token abcdefghijklmnopqrstuvwxyz

##### &emsp;&emsp;URL:

##### &emsp;&emsp;&emsp;&emsp;/auth/register/

##### &emsp;&emsp;REQUEST:

```
	"email": string,
	"password": string, (max-15, min-5) // This is frontend validation in vatisum (5-15)
```

##### &emsp;&emsp;RESPONSE:

```
	"success": boolean,
	"errors": dict,
	"tokens": dict, // jwt access, refresh tokens
	"otp": int,// 4 digit otp
```
##### IMAGE:
![Image](/static/register.png)

##### &emsp;&emsp;EXAMPLES:

##### &emsp;&emsp; &emsp;&emsp;CASE 1: User created and send otp to corresponding mail

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email":"ilmnmukesh@gmail.com",
            "password": "Nones"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 200

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
	{
            "success": true,
            "errors": {},
            "tokens": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.....", // secure purpose remove token
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...." // secure purpose remove token
            },
            "otp": 3633
	}
```

##### &emsp;&emsp; &emsp;&emsp;CASE 2: User already registered

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email":"ilmnmukesh@gmail.com",
            "password": "Nones"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
	{
            "success": false,
            "errors": {
                "errors": [
                    "ilmnmukesh@gmail.com is already register with us"
                ]
            },
            "tokens": {}
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 3: Other errors

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email":"ilmnmukesh@gmail.com"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "errors": {
                "password": [
                    "This field is required."
                ]
            },
            "tokens": {}
        }
```

##### Similarly for email and email validation

### 2. Google Register:

##### &emsp;&emsp;METHOD: POST

##### &emsp;&emsp;HEADERS:

##### &emsp;&emsp;&emsp;&emsp;Authorization: Token abcdefghijklmnopqrstuvwxyz

##### &emsp;&emsp;URL:

##### &emsp;&emsp;&emsp;&emsp;/auth/register/google/

##### &emsp;&emsp;REQUEST:

```
	auth_token:"encrypt data from google" id_token
```

##### &emsp;&emsp;RESPONSE:

```
	"success": boolean,
	"errors": dict,
	"tokens": dict, // jwt access, refresh tokens
```
##### IMAGE:
![Image](/static/google_register.png)

##### Using auth_token, server will fetch from google and google returns the corresponding user details. Validate using that email from google. Once validate completes, move on to main page using JWT access and refresh token.

##### &emsp;&emsp;EXAMPLES:

##### &emsp;&emsp; &emsp;&emsp;CASE 1: User created

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_token":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 200

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": true,
            "errors": {},
            "tokens": {
                "access_token": "eyJ0eXAiaQicMt-d2X8NRF2....aW2Hi5wqg",
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc.....VGQcLAQs"
            }
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 2: User already registered

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_token":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "errors": {
                "auth_token": [
                    "ilmnmukesh@gmail.com is already register with us"
                ]
            },
            "tokens": {}
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 3: Token error or expired

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_token":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "errors": {
                "auth_token": [
                    "The Token is invalid or has expired"
                ]
            },
            "tokens": {}
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 4: Other errors

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_tokens":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
       {
            "success": false,
            "errors": {
                "auth_token": [
                    "This field is required."
                ]
            },
            "tokens": {}
	}
```

### 3. Normal Login:

##### &emsp;&emsp;METHOD: POST

##### &emsp;&emsp;HEADERS:

##### &emsp;&emsp;&emsp;&emsp;Authorization: Token abcdefghijklmnopqrstuvwxyz

##### &emsp;&emsp;URL:

##### &emsp;&emsp;&emsp;&emsp;/auth/login/

##### &emsp;&emsp;REQUEST:

##### &emsp;&emsp;REQUEST:

```
	"email": string,
	"password": string,//not like signup min and max not there
```

##### &emsp;&emsp;RESPONSE:

```
	"success": boolean,
	"errors": dict,
	"tokens": dict, // jwt access, refresh tokens
	"is_verified": boolean
```

##### IMAGE:
![Image](/static/login.png)

##### &emsp;&emsp;EXAMPLES:

##### &emsp;&emsp; &emsp;&emsp;CASE 1: User details validate success and email verified

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email": "ilmnmukesh@gmail.com",
            "password":"Nones"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 200

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": true,
            "is_verified": true,
            "tokens": {
                "access_token": "eyJ0eXAiaQicMt-d2X8NRF2....aW2Hi5wqg",
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc.....VGQcLAQs"
            },
            "errors": {}
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 2: User details validate success and email is not verified. OTP sent to mail

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email": "ilmnmukesh@gmail.com",
            "password":"Nones"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 200

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": true,
            "is_verified": false,
            "tokens": {
                "access_token": "eyJ0eXAiaQicMt-d2X8NRF2....aW2Hi5wqg",
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc.....VGQcLAQs"
            },
            "errors": {},
            "otp":2023
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 3: User registered with gmail and wrong password entered

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email": "ilmnmukesh1@gmail.com",
            "password":"Nones"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "is_verified": false,
            "tokens": {},
            "errors": {
                "email": [
                    "E-mail doesn't exists"
                ],
                "description": "Invaild Email / Password. Try again"
            }
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 4: User registered but password wrong

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email": "ilmnmukesh@gmail.com",
            "password":"Noness"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "is_verified": false,
            "tokens": {},
            "errors": {
                "password": [
                    "Password mismatch"
                ],
                "description": "Invaild Email / Password. Try again"
            }
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 5: User not yet registered

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
            "email": "ilmnmukesh@gmail.com",
            "password":"Noness"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "is_verified": false,
            "tokens": {},
            "errors": {
                "email": [
                    "E-mail doesn't exists"
                ],
                "description": "Invaild Email / Password. Try again"
            }
        }
```

### 4. Google Login:

##### &emsp;&emsp;METHOD: POST

##### &emsp;&emsp;HEADERS:

##### &emsp;&emsp;&emsp;&emsp;Authorization: Token abcdefghijklmnopqrstuvwxyz

##### &emsp;&emsp;URL:

##### &emsp;&emsp;&emsp;&emsp;/auth/login/google/

##### &emsp;&emsp;REQUEST:

```
	auth_token:"encrypt data from google" id_token
```

##### &emsp;&emsp;RESPONSE:

```
	"success": boolean,
	"errors": dict,
	"tokens": dict, // jwt access, refresh tokens
```

##### IMAGE:
![Image](/static/google_login.png)

##### Using auth_token, server will fetch from google and google returns the corresponding user details. Validate using that email from google. Once validate completes, move on to main page using JWT access and refresh token.

##### &emsp;&emsp;EXAMPLES:

##### &emsp;&emsp; &emsp;&emsp;CASE 1: User details validate success. Also, if normal register user which is not verify there email means update automatically.

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_token":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 200

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": true,
            "errors": {},
            "tokens": {
                "access_token": "eyJ0eXAiaQicMt-d2X8NRF2....aW2Hi5wqg",
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc.....VGQcLAQs"
            }
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 2: User not found

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_token":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "tokens": {},
            "errors": {
                "auth_token": [
                    "smileymukesh436@gmail.com is not register with us. Kindly share the verified email."
                ]
            }
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 3: Token error or expired

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"auth_token":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
	{
            "success": false,
            "errors": {
                "auth_token": [
                    "The Token is invalid or has expired"
                ]
            },
            "tokens": {}
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 4: Other errors

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"ath_tokens":"eyJhbGciOiJSUzI......N08e7ww"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "errors": {
                "auth_token": [
                    "This field is required."
                ]
            },
            "tokens": {}
        }
```

### 5. Resend OTP:

##### &emsp;&emsp;METHOD: POST

##### &emsp;&emsp;HEADERS:

##### &emsp;&emsp;&emsp;&emsp;Authorization: Token abcdefghijklmnopqrstuvwxyz

##### &emsp;&emsp;URL:

##### &emsp;&emsp;&emsp;&emsp;/auth/resend/otp/

##### &emsp;&emsp;REQUEST:

```
	email:string, "valid e-mail is required"
```

##### &emsp;&emsp;RESPONSE:

```
	"success": boolean,
	"errors": dict,
	"otp": int, // four digit number
```

##### IMAGE:
![Image](/static/resend.png)

##### &emsp;&emsp; &emsp;&emsp;CASE 1: Email successfully send

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"email":"ilmnmukesh@gmail.com"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 200

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": true,
            "otp": 0217,
            "errors": {}
        }
```

##### &emsp;&emsp; &emsp;&emsp;CASE 2: Email didn't validated

##### &emsp;&emsp; &emsp;&emsp;INPUT:

```
        {
		"email":"ilmnmmmm@a.com"
        }
```

##### &emsp;&emsp; &emsp;&emsp;OUTPUT:

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;STATUS: 400

##### &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;JSON RESULT:

```
        {
            "success": false,
            "otp": 0,
            "errors": {
                "email": [
                    "Enter a valid email address."
                ]
            }
        }
```
