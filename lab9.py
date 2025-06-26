from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MovieRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500))

def init_db():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = int(request.form['rating'])
        review = request.form['review']
        
        if title and genre and 1 <= rating <= 5:
            new_rating = MovieRating(
                title=title,
                genre=genre,
                rating=rating,
                review=review
            )
            db.session.add(new_rating)
            db.session.commit()
        
        return redirect(url_for('index'))
    
    ratings = MovieRating.query.order_by(MovieRating.rating.desc()).all()
    return render_template('index.html', ratings=ratings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)