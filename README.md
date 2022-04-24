# Assignment 1

This project is an minmalistic HTTP server to serve a password protected website which enables the user to manage their investment porfolio.

## Instructions

 Extract the zip file 
## Run Locally

Open the Powershell or CMD and open the directory

```bash
  cd my-project
```

Run the python server

```bash
  python3 server3.py
```

Copy the localhost link to a browser. 

The default html file of the server is the portfolio.html

```bash
  http://localhost:8080
```

To directly open the research.html
```bash
  http://localhost:8080/research.html
```


## Run in Dockerfile
You can run this project using docker itself. 

Open your powershell and open the directory
```bash
  cd my-project
```
Build 
```bash
  docker build . -t server3
```
Run 
```bash
  docker run -p 8080:8080 server3:latest
```
Copy and Paste the http link to a browser

```bash
  http://localhost:8080
```
## Run using Heroku

Open your powershell and open the directory
```bash
  cd my-project
```
Login to heroku
```bash
  heroku login
```
Login to the container
```bash
  heroku container:login
```
Push the Docker-based app
```bash
  heroku container:push web
```
Deploy the changes 
```bash
  heroku container:release web
```
Open the app 
```bash
  heroku open
```

You can either open the app using the link below: 

https://assignmen1-159352.herokuapp.com/
## Useful Documentation

[IEX Docs](https://iexcloud.io/docs/api/#api-reference)

[Docker Docs](https://docs.docker.com)

[Heroku DevCenter](https://devcenter.heroku.com)
