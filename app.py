from flask import Flask

app = Flask(__name__)

app.run(host='zlbweb.cn', port=443, ssl_context=('cert.pem', 'key.pem'))
