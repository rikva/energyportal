from flask import Flask, request, json

app = Flask(__name__)


@app.route('/input', methods=['POST'])
def post():
    print(request.data)
    print(json.loads(request.data))
    return "OK", 201


if __name__ == '__main__':
    app.run()
