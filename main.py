from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # База данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Объект класса SQLAlchemy


class Article(db.Model):  # Создаем бъявления для базы данныой
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(20), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        user = request.form['user']
        price = request.form['price']

        article = Article(title=title, text=text, user=user, price=price)

        try:
            db.session.add(article)
            db.session.commit()
            #return 'Объявление успешно добавлено!'
            return redirect('/home')
        except:
             return 'При добавлении объявления произошла ошибка!'
    else:
        return render_template("create.html")


@app.route('/home/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()

        return redirect('/home')
    except:
        return 'При добавлении объявления произошла ошибка!'


@app.route('/home/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    article = Article.query.get(id)

    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']
        article.user = request.form['user']
        article.price = request.form['price']
        #data = request.form['data']

        try:
            db.session.commit()
            #return 'Объявление успешно добавлено!'
            return redirect('/home')
        except:
             return 'При редактировании объявления произошла ошибка!'
    else:

        return render_template("update.html", article=article)


@app.route('/home')
def posts():
    articles = Article.query.order_by(Article.data).all()
    #print(articles)
    return render_template("posts.html", articles=articles)   # articles - работа со списком в шаблоне


@app.route('/home/<int:id>')
def post_det(id):
    article = Article.query.get(id)
    return render_template("postd.html", article=article)

# @app.route('/reg')
# def reg():
#     pass

if __name__ == "__main__":
    app.run(debug=True)


