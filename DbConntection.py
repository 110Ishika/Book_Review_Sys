from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)

# PostgreSQL URI format:
# postgresql://<username>:<password>@<host>:<port>/<database>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Root@localhost:5432/Book_Store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cache = Cache(app)


if __name__ == '__main__':
    app.run(debug=True)