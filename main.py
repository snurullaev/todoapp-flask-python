# Импорт необходимых модулей
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Инициализация Flask-приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'  # Указание пути к базе данных SQLite
db = SQLAlchemy(app)  # Инициализация SQL базы данных в приложении

# Создание модели Post для хранения постов
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Поле id как первичный ключ
    title = db.Column(db.String(100), nullable=False)  # Поле для заголовка поста
    content = db.Column(db.Text, nullable=False)  # Поле для содержимого поста

# Маршрут для главной страницы
@app.route('/')
def home():
    posts = Post.query.all()  # Запрос для получения всех постов из базы данных
    return render_template('index.html', posts=posts)  # Отображение шаблона index.html с передачей списка постов

# Маршрут для создания нового поста
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':  # Если форма отправлена методом POST
        title = request.form['title']  # Получение заголовка из формы
        content = request.form['content']  # Получение содержимого из формы
        new_post = Post(title=title, content=content)  # Создание нового объекта Post
        db.session.add(new_post)  # Добавление поста в сессию базы данных
        db.session.commit()  # Подтверждение изменений
        return redirect(url_for('home'))  # Переадресация на главную страницу
    return render_template('create.html')  # Отображение формы создания поста

if __name__ == 'main':  # Если это основной файл
    with app.app_context():
        db.create_all()  # Создание таблиц базы данных, если их еще нет
    app.run(debug=True)  # Запуск Flask-приложения в режиме отладки
