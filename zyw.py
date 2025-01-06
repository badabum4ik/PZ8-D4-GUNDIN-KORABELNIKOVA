import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'ex45rct6v7ybu8ni'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Название маршрута для входа

# Словарь пользователей для демонстрации
users = {
    "Rukovodstvo": {"password": "Rukovodstvopassword", "role": "Rukovodstvo"},
    "Uprava": {"password": "Upravapassword", "role": "Uprava"}
}

# Модель пользователя
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]["role"]

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверка логина и пароля
        if username in users and users[username]['password'] == password:
            user = User(username=username)
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Неправильное имя пользователя или пароль', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/stat', methods=['GET'])
@login_required
def statistics():
    if current_user.role != 'Rukovodstvo':
        return '''
        <html>
            <body style="text-align: center; padding: 50px;">
                <h1 style="color: orange; text-align: center; font-size: 120px;">Доступ запрещен</h1>
                <p style="font-size: 30px;">Попроси пароль у руководителя</p>
            </body>
        </html>
        ''', 403


    conn = sqlite3.connect('new_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    data = cursor.fetchall()
    conn.close()
    return render_template('stat.html', new_database=data)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)