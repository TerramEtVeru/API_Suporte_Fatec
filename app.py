from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql

app = Flask(__name__)

#conn = sql.connect('database.db')
#conn.execute('DROP TABLE reports')
#conn.execute('CREATE TABLE reports (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, pc TEXT, sala TEXT, desc TEXT)')
#conn.close()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', msg = "")

@app.route('/admin')
def admin():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM reports")
    rows = cur.fetchall()
    return render_template('admin.html', username='', rows = rows)

@app.route('/address', methods = ['POST', 'GET'])
def address():
   if request.method == 'POST':
      try:
         pc = request.form['pc']
         sala = request.form['sala']
         desc = request.form['desc']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO reports (data,pc,sala,desc) VALUES (datetime('now'),?,?,?)",(pc,sala,desc))
            con.commit()
            msg = "Enviado com sucesso"
      except:
         con.rollback()
         msg = "ERRO: ENTRAR EM CONTATO COM OS DESENVOLVEDORES"
      
      finally:
         return render_template("index.html", msg = msg)
         con.close()

if __name__ == '__main__':
    app.run(debug=True)
