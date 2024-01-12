from flask import Flask, render_template, request, redirect, url_for
import sqlite3


# SQLite veritabanı bağlantısı oluşturma
conn = sqlite3.connect('score_table.db')
cursor = conn.cursor()


# Kullanıcılar tablosunu oluşturma
# id =  kullanıcı no
# user = kullanıcı adı
# score = sınav notu
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        score INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()


# Uygulamayı oluşturma
app = Flask(__name__)


# Anasayfa
@app.route("/")
def index():
    # Anasayfayı açtığında en iyi skoru yükleme
    conn = sqlite3.connect('score_table.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users ORDER BY score DESC LIMIT 1')
    best_score = cursor.fetchall()

    cursor.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    last_score = cursor.fetchall()

    conn.close()

    # Veritabında kayıt olup olmadığını kontrol etme
    if len(best_score) == 0:
        user2 = "Unnamed"
        score2 = 0
        last_score = 0
    else:
        user2 = best_score[0][1]
        score2 = int(best_score[0][2])

        last_score = last_score[0][2]

    return render_template("index.html", the_score = score2, the_user = user2, your_score=last_score)


# Cevapları değerlendirme ve skoru veritabanına kaydetme
@app.route('/save_score', methods=['POST'])
def save_score():
    if request.method == 'POST':
        user = request.form['user']
        answer_1 = request.form['question_1']
        answer_2 = request.form['question_2']
        answer_3 = request.form['question_3']
        answer_4 = request.form['question_4']

        # Cevapları değerlendirme
        score = 0
        if answer_1 == "Correct":
            score += 25
        if answer_2 == "Correct":
            score += 25
        if answer_3 == "Correct":
            score += 25
        if answer_4 == "Correct":
            score += 25


        # Veritabanına kaydetme
        conn = sqlite3.connect('score_table.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user, score) VALUES (?, ?)', (user, score))
        conn.commit()

    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)


