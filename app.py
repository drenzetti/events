from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'events.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(80), nullable=False)

    def __init__(self, title, desc, date):
        self.title = title
        self.desc = desc
        self.date = date

    def serialize(self):
       return {
           'title' : self.title,
           'desc': self.desc,
           'date'  : self.date
       }

class EventSchema(ma.Schema):
    class Meta:
        fields = ('title', 'desc', 'date')

event_schema = EventSchema()
events_schema = EventSchema(many=True)

# Create Event
@app.route("/events/", methods=["POST"])
def add_event():
    title = request.form['title']
    desc = request.form['desc']
    date = request.form['date']

    new_event = Event(title, desc, date)

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.serialize())

# Show Events
@app.route("/events/", methods=["GET"])
def get_event():
    all_events = Event.query.all()
    result = events_schema.dump(all_events)
    return jsonify(result.data)

# Edit Events
@app.route("/events/<int:id>", methods=["PUT"])
def event_update(id):
    event = Event.query.get(id)
    title = request.form['title']
    desc = request.form['description']
    date = request.form['date']

    event.title = title
    event.desc = desc
    event.date = date

    db.session.commit()
    return event_schema.jsonify(event)

# Delete Events
@app.route("/events/<int:id>", methods=["DELETE"])
def event_delete(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()

    return event_schema.jsonify(event)

if __name__ == '__main__':
    app.run(debug=True)
