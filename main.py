from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db= SQLAlchemy(app)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(50), nullable = False)
    album = db.Column(db.String(50), nullable = False)
    year = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return {
            "id" : self.id,
            "artist" : self.artist,
            "album" : self.album,
            "year" : self.year
        }

with app.app_context():
    db.create_all()


# Create Routes
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Music API"})

@app.route("/albums", methods=["GET"])
def get_artists():
    albums = Album.query.all()

    return jsonify([album.to_dict() for album in albums])

@app.route("/albums/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    artist = Album.query.get(artist_id)
    if artist:
        return jsonify(artist.to_dict())
    else:
        return jsonify({"error":"Artist not found!"}), 404

# POST
@app.route("/albums", methods=["POST"])
def add_album():    
    data= request.get_json()

    new_album = Album(artist=data["artist"],
                                  album=data["album"],
                                  year=data["year"])

    db.session.add(new_album)
    db.session.commit()

    return jsonify(new_album.to_dict()), 201


# PUT
@app.route("/albums/<int:artist_id>", methods=["PUT"])
def update_artist(artist_id):
    data=request.get_json()

    artist = Album.query.get(artist_id)
    if artist:
        artist.artist = data.get("artist", artist.artist)
        artist.album = data.get("album", artist.country)
        artist.year = data.get("year", artist.rating)

        db.session.commit()

        return jsonify(artist.to_dict())

    else:
        return jsonify({"error":"Artist not found!"}), 404


# DELETE
@app.route("/albums/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    artist = Album.query.get(artist_id)
    if artist:
        db.session.delete(artist)
        db.session.commit()

        return jsonify({"message":"Artist was deleted"})
    
    else:
        return jsonify({"error":"Artist not found!"}), 404



if __name__ == "__main__":
    app.run(debug=True)