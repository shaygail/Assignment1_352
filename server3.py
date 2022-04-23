## Shayenne Galiste
## Server

from socket import *
import _thread

# added
import base64
import json

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
# Server should be up and running and listening to the incoming connections
print(f"The server is running at http://localhost:{serverPort}")

# Extract the given header value from the HTTP request message
def getHeader(message, header):
    if message.find(header) > -1:
        value = message.split(header)[1].split()[0]
    else:
        value = None

    return value


# service function to fetch the requested file, and send the contents back to the client in a HTTP response.
def getFile(filename):
    try:
        # open and read the file contents. This becomes the body of the HTTP response
        f = open(filename, "rb")
        body = f.read()
        header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
    except IOError:
        # Send HTTP response message for resource not found
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = (
            "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()
        )

    return header, body


# default service function
def default(message, resource):
    username = "19042232"
    password = "19042232"
    credentials = f"{username}:{password}"

    token = getHeader(message, "Authorization: Basic ")
    if token != None:
        userpass = base64.b64decode(token).decode()
        if userpass == credentials:
            print("Authenticated!")
            # map requested resource (contained in the URL) to specific function which generates HTTP response
            if resource == "" or resource == "portfolio":
                return getFile("portfolio.html")
            elif resource == "research":
                return getFile("research.html")
            else:
                return getFile(resource)
        else:
            print("Incorrect Username or Password.")
    return authenticate()


# asks user for credentials
def authenticate():
    header = "HTTP/1.1 401 Unauthorized\nWWW-Authenticate: Basic realm='myRealm'\r\n\r\n".encode()
    body = "<html><head></head><body>Login</body></html>\r\n".encode()

    return header, body


# opens alert with error message
def error_message(error):
    return f"<script>alert('{error}')</script>\r\n".encode()


# checks user submitted a form
# parses and saves the data
def receive_form(message):
    form = getHeader(message, "symbol")
    if form != None:
        formdata = [param_expr.split("=", 1) for param_expr in form.split("&")]
        stock = {}
        stock["symbol"] = formdata[0][1].upper()
        stock["quantity"] = int(formdata[1][1])
        if stock["quantity"] > 0:
            stock["price"] = int(formdata[2][1])

        print("Data received.")
        write_json(stock)


# writes the data to portfolio.json
def write_json(data):
    with open("portfolio.json") as json_file:
        portfolio = json.load(json_file)

        portfolio = validate(data, portfolio)

        new_data = json.dumps(portfolio)
        with open("portfolio.json", "w") as new_json:
            new_json.write(new_data)
            print("Data written to file.")


# checks if quantity is positive, zero or negative
# manipulates data accordingly
def validate(data, portfolio):
    print("Validating data.")
    # if negative quantity
    if data["quantity"] <= 0:
        for index, stocks in enumerate(portfolio["stocks"]):
            if stocks["symbol"] == data["symbol"]:
                if abs(data["quantity"]) > portfolio["stocks"][index]["quantity"]:
                    raise (Exception("Error short selling not allowed."))
                portfolio["stocks"][index]["quantity"] += data["quantity"]
                if portfolio["stocks"][index]["quantity"] == 0:
                    portfolio["stocks"].pop(index)
                break
    # if positive quantity
    else:
        for index, stocks in enumerate(portfolio["stocks"]):
            if stocks["symbol"] == data["symbol"]:

                new_price = calculate_price(portfolio["stocks"][index], data)

                portfolio["stocks"][index]["quantity"] += data["quantity"]
                portfolio["stocks"][index]["price"] = new_price

                if portfolio["stocks"][index]["quantity"] == 0:
                    portfolio["stocks"].pop(index)
                break
        # execute if for loop did not break
        else:
            portfolio["stocks"].append(data)

    return portfolio


# calculates new price if adding same symbol to portfolio
def calculate_price(portfolio_stock, data):
    quantityA = portfolio_stock["quantity"]
    priceA = portfolio_stock["price"]
    quantityB = data["quantity"]
    priceB = data["price"]
    new_price = (quantityA * priceA + quantityB * priceB) / (quantityA + quantityB)
    return round(new_price, 2)


# We process client request here. The requested resource in the URL is mapped to a service function which generates the HTTP reponse
# that is eventually returned to the client.
def process(connectionSocket):
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()
    except Exception:
        print("Timeout")

    if len(message) > 1:
        # Extract the path of the requested object from the message
        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character
        resource = message.split()[1][1:]

        responseHeader, responseBody = default(message, resource)

        # Send the HTTP response header line to the connection socket
        connectionSocket.send(responseHeader)
        # Send the content of the HTTP body (e.g. requested file) to the connection socket
        connectionSocket.send(responseBody)
        try:
            receive_form(message)
        except Exception as e:
            print(e)
            connectionSocket.send(error_message(e))
        # Close the client connection socket
        connectionSocket.close()


# Main web server loop. It simply accepts TCP connections, and get the request processed in seperate threads.
while True:
    # Set up a new connection from the client
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    # Clients timeout after 60 seconds of inactivity and must reconnect.
    connectionSocket.settimeout(60)
    # start new thread to handle incoming request
    _thread.start_new_thread(process, (connectionSocket,))
