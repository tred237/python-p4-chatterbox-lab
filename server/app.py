from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

import ipdb

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            messages.append(message.to_dict())
        return make_response(
            messages,
            200
        )
    elif request.method == 'POST':
        message = Message(
            username = request.get_json().get('username'),
            body = request.get_json().get('body')
        )
        db.session.add(message)
        db.session.commit()
        return make_response(
            message.to_dict(),
            201
        )

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'PATCH':
        for attribute in request.get_json():
            setattr(message, attribute, request.get_json().get(attribute))
        db.session.add(message)
    elif request.method == 'DELETE':
        db.session.delete(message)

    db.session.commit()
    return make_response(
        message.to_dict(),
        200
    )

if __name__ == '__main__':
    app.run(port=5555)
