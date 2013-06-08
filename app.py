import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    print "Printing hello world!"
    return 'Hi World!'

if __name__ == '__main__':
    # Bind to PORT if defined, else default to 5000.
    port = int(os.environ.get('PORT', 5000))

    # Run the app.
    app.run(host='0.0.0.0', port=port)
