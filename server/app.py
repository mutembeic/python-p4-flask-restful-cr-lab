#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

# Define the Plant model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.Float)

    def __init__(self, name, image, price):
        self.name = name
        self.image = image
        self.price = price

# Index Route - Get a list of all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    plant_list = [{"id": plant.id, "name": plant.name, "image": plant.image, "price": plant.price} for plant in plants]
    return jsonify(plant_list)

# Show Route - Get a specific plant by ID
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if plant:
        return jsonify({"id": plant.id, "name": plant.name, "image": plant.image, "price": plant.price})
    else:
        return jsonify({"error": "Plant not found"}), 404

# Create Route - Create a new plant
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    name = data.get('name')
    image = data.get('image')
    price = data.get('price')

    if not name or not image or not price:
        return jsonify({"error": "Invalid data"}), 400

    new_plant = Plant(name=name, image=image, price=price)
    db.session.add(new_plant)
    db.session.commit()

    return jsonify({"id": new_plant.id, "name": new_plant.name, "image": new_plant.image, "price": new_plant.price}), 201

if __name__ == '__main__':
    app.run(debug=True)
