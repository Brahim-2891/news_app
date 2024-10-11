from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Text, DateTime
from datetime import datetime
import datetime 


app =  Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'

app.config['SECRET_KEY'] = 'Brahim@1982Xyza'

db = SQLAlchemy()
db.init_app(app)


class News(db.Model):
    __tablename__ = "News"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now(), nullable=False)
    article: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_news = News.query.all()
    # result = db.session.execute(db.select(News))
    # all_news = result.scalars().all()
    return render_template('home.html',all_news=all_news) 

# Function to add new news to the database
def add_new_news(title: str, article: str, img_url: str):
    new_news = News(
        title=title,
        article=article,
        img_url=img_url,
        date=datetime.datetime.now()  # Automatically add current datetime
    )
    
    db.session.add(new_news)  # Add the new news item to the session
    db.session.commit()       # Commit the session to write the changes to the database
    print(f"News '{title}' has been added successfully.")



# @app.route('/show_news')
# def show_news():
#     # Fetch all news from the News table
#     all_news = News.query.all()
    
#     # Render the 'show_news.html' template and pass the news data
#     return render_template('show_news.html', all_news=all_news)


@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        article = request.form.get('article')
        img_url = request.form.get('img_url')
        
        # Check if all fields are filled
        if not title or not article or not img_url:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_new'))

        # Add new news to the database
        new_news = News(
            title=title,
            article=article,
            img_url=img_url,
            date=datetime.datetime.now()
        )
        db.session.add(new_news)
        db.session.commit()

        flash('News added successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to the list of news after submission

    # For GET request, just render the form
    return render_template('add_new.html')


@app.route('/news/<int:news_id>')
def read_news(news_id):
    # Fetch the specific news article by ID
    news = News.query.get_or_404(news_id)
    
    # Render a template to display the news article
    return render_template('read_news.html', news=news)

@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    # Fetch the news article by ID
    news = News.query.get_or_404(news_id)
    
    if request.method == 'POST':
        # Update news data based on form input
        news.title = request.form['title']
        news.article = request.form['article']
        news.img_url = request.form['img_url']
        
        db.session.commit()  # Save the changes to the database
        
        flash('News updated successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to the homepage
    
    # Render the edit form with current news data
    return render_template('edit_news.html', news=news)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
