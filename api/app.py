from flask import Flask
from data import alchemy
from dotenv import load_dotenv
import os

load_dotenv()

print(f'{os.getenv("ACCESS_TOKEN")}')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXEPTION'] = True

@app.before_first_request
def create_tables():
  alchemy.create_all()

@app.route('/', methods=["GET"])
def home():
  return "API funcionando", 200

app.run(port=5000, debug=True)