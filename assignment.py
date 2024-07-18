#Task 1, 2, 3

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:654U7jsv@localhost/videos'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

class MovieSchema(ma.Schema):
    title = fields.String(required=True)

    class Meta:
        fields = ('title', 'id')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return movies_schema.jsonify(movies)

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid]['title'] == target:
            return arr[mid]
        elif arr[mid]['title'] < target:
            low = mid + 1
        else:
            high = mid - 1

    return None

@app.route('/movies/sorted', methods=['GET'])
def get_sorted_movies():
    movies = Movie.query.all()
    movies_list = movies_schema.dump(movies)
    sorted_movies = merge_sort(movies_list)
    return jsonify(sorted_movies)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    sorted_arr = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]['title'].lower() <= right[j]['title'].lower():
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1

    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])

    return sorted_arr

@app.route('/binary-search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    movies = Movie.query.order_by(Movie.title).all()
    movies_list = movies_schema.dump(movies)

    result = binary_search(movies_list, query)
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No movies found with that title"}), 404
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)