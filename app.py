from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'techtrek.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Add these new models to your app.py
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    featured = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(500), nullable=False)

    def __init__(self, title, instructor, price, rating, rating_count, featured=False, image_url="/api/placeholder/280/160"):
        self.title = title
        self.instructor = instructor
        self.price = price
        self.rating = rating
        self.rating_count = rating_count
        self.featured = featured
        self.image_url = image_url

class Testimonial(db.Model):
    __tablename__ = "testimonials"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)

    def __init__(self, content, student_name, student_title, image_url="/api/placeholder/80/80"):
        self.content = content
        self.student_name = student_name
        self.student_title = student_title
        self.image_url = image_url

# Update your index route to fetch featured courses and testimonials
@app.route("/")
def index():
    featured_courses = Course.query.filter_by(featured=True).limit(3).all()
    testimonials = Testimonial.query.limit(3).all()
    return render_template("index.html", featured_courses=featured_courses, testimonials=testimonials)

# Add this code block after your db creation to add sample data
def add_sample_data():
    # Add sample courses if none exist
    if Course.query.count() == 0:
        sample_courses = [
            Course("Complete Python Bootcamp", "John Smith", 49.99, 4.5, 1250, True),
            Course("React.js Advanced Concepts", "Sarah Johnson", 59.99, 5.0, 850, True),
            Course("Full-Stack Web Development", "Mike Wilson", 69.99, 4.0, 2000, True)
        ]
        for course in sample_courses:
            db.session.add(course)

    # Add sample testimonials if none exist
    if Testimonial.query.count() == 0:
        sample_testimonials = [
            Testimonial(
                "The Python Bootcamp was exactly what I needed to transition into a career in data science. The instructor's teaching style made complex concepts easy to understand.",
                "Alex Thompson",
                "Data Scientist at Tech Corp"
            ),
            Testimonial(
                "I went from knowing nothing about web development to building full-stack applications. The step-by-step approach and project-based learning was incredible.",
                "Emily Rodriguez",
                "Frontend Developer"
            ),
            Testimonial(
                "The React.js course helped me level up my development skills. The advanced concepts section was particularly helpful for my current role.",
                "David Chen",
                "Senior Web Developer"
            )
        ]
        for testimonial in sample_testimonials:
            db.session.add(testimonial)

    db.session.commit()

# Add this line after db.create_all()
with app.app_context():
    db.create_all()
    add_sample_data()
# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blog", methods=["GET", "POST"])
def blog():
    return render_template("blog.html")

@app.route("/careers", methods=["GET", "POST"])
def careers():
    return render_template("careers.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(debug=True)