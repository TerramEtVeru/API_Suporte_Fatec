from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql

app = Flask(__name__)

#conn = sql.connect('database.db')
#conn.execute('DROP TABLE salas')
#conn.execute('CREATE TABLE salas (nome TEXT, elements TEXT, total INTEGER)')
#conn.close()

@app.route('/')
@app.route('/home')
def home():
   return render_template('/home.html')

@app.route('/report')
def report():
   return render_template('/report.html')

@app.route('/index', methods = ['POST', 'GET'])
def index():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT nome FROM salas")
   rows = cur.fetchall()
   return render_template('index.html', rows = rows)

@app.route('/address', methods = ['POST', 'GET'])
def address():
   elmnts = ""
   if request.method == 'POST':
      try:
         selected = request.form["selectedvalue"]

         if (request.form['actiontype'] == "add"):
            nome = request.form['txtnew']
            elements = request.form['elementcontent']
            total = request.form['totalcontent']
            with sql.connect("database.db") as con:
               cur = con.cursor()
               cur.execute('INSERT INTO salas (nome, elements, total) VALUES (?, ?, ?)',(nome, elements, total))
               con.commit()
               msg = "Sala criada com sucesso"

         elif (request.form['actiontype'] == "del"):
            nome = request.form['salalist']
            with sql.connect("database.db") as con:
               cur = con.cursor()
               cur.execute("DELETE FROM salas WHERE nome="+nome)
               con.commit()
               msg = "Sala delatada com sucesso"

         elif (request.form['actiontype'] == "save"):
            nome = request.form['salalist']
            elements = request.form['elementcontent']
            total = request.form['totalcontent']
            with sql.connect("database.db") as con:
               cur = con.cursor()
               cur.execute("UPDATE salas SET elements = ?, total = ? WHERE nome="+nome,(elements, total))
               con.commit()
               msg = "Sala modificada com sucesso"

               nome = request.form['salalist']
               with sql.connect("database.db") as con:
                  con.row_factory = sql.Row
                  cur = con.cursor()
                  cur.execute("SELECT * FROM salas WHERE nome="+nome)
                  elmnts = cur.fetchall()

         elif (request.form['actiontype'] == "load"):
            nome = request.form['salalist']
            with sql.connect("database.db") as con:
               con.row_factory = sql.Row
               cur = con.cursor()
               cur.execute("SELECT * FROM salas WHERE nome="+nome)
               elmnts = cur.fetchall()
               msg = "Sala carregada com sucesso"

      except:
         con.rollback()
         msg = ("ERRO")

      finally:
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("SELECT nome FROM salas")
         rows = cur.fetchall()
         return render_template("index.html", rows = rows, selected = selected, msg = msg, elmnts = elmnts)
         con.close()

@app.route('/sala')
def sala():
      nome = "302"
      #carregar todas as salas, e depois de carregar elas
      with sql.connect("database.db") as con:
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("SELECT * FROM salas")
         rows = cur.fetchall()
         msg = "Sala carregada com sucesso"
         return render_template("sala.html", rows = rows)
         con.close()
         
@app.route('/admin')
def admin():
   return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
