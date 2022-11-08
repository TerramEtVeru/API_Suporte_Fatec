from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql

app = Flask(__name__)

#conn = sql.connect('database.db')
#conn.execute('DROP TABLE salas')
#conn.execute('CREATE TABLE salas (nome TEXT, elements TEXT, total INTEGER)')
#conn.close()

#conn = sql.connect('database.db')
#conn.execute('DROP TABLE problemas')
#conn.execute('CREATE TABLE problemas (id INTEGER PRIMARY KEY AUTOINCREMENT, problema TEXT, sugestao TEXT)')
#conn.close()

#conn = sql.connect('database.db')
#conn.execute('DROP TABLE reports')
#conn.execute('CREATE TABLE reports (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, sala TEXT, pc TEXT, desc TEXT, problema TEXT, classificacao TEXT, arquivados TEXT)')
#conn.close()


#conn = sql.connect('database.db')
#conn.execute('DROP TABLE arquivados')
#conn.execute('CREATE TABLE arquivados (id INTEGER PRIMARY KEY AUTOINCREMENT, idoriginal INTEVER, data TEXT, sala TEXT, pc TEXT, desc TEXT, problema TEXT, classificacao TEXT, resolucao TEXT)')
#conn.close()

@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
   with sql.connect("database.db") as con:
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("SELECT * FROM salas")
         rows = cur.fetchall()
         
         cur.execute("SELECT * FROM problemas")
         problemas = cur.fetchall()

         return render_template("index.html", rows = rows, problemas = problemas)
         con.close()

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
   with sql.connect("database.db") as con:
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("SELECT * FROM reports WHERE NOT arquivados = ?",("sim",))
         rows = cur.fetchall()
         return render_template("admin.html", rows = rows)
         con.close()

@app.route('/send', methods = ['POST', 'GET'])
def send():
   if request.method == 'POST':
      try:
         sala = request.form['sala']
         pc = request.form['computador']
         desc = request.form['descricao']
         problema = request.form['problema']
         classificacao = request.form['classificacao']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO reports (data,pc,sala,desc,problema,classificacao,arquivados) VALUES (datetime('now'),?,?,?,?,?,?)",(pc,sala,desc,problema,classificacao,"false"))
            con.commit()
      except:
         con.rollback()
      finally:
         return render_template("index.html")
         con.close()

@app.route('/update', methods = ['POST', 'GET'])
def update():
   option = request.form['options']
   with sql.connect("database.db") as con:
      cur = con.cursor()
      cur.execute("UPDATE reports SET arquivados = ? WHERE id="+option,("sim",))
      con.commit()

      with sql.connect("database.db") as con:
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("SELECT * FROM reports WHERE NOT arquivados = ?",("sim",))
         rows = cur.fetchall()

         return render_template("admin.html", rows = rows)
         con.close()

@app.route('/edit', methods = ['POST', 'GET'])
def edit():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT nome FROM salas")
   rows = cur.fetchall()
   return render_template('edit.html', rows = rows)

@app.route('/edited', methods = ['POST', 'GET'])
def edited():
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
         return render_template("edit.html", rows = rows, selected = selected, msg = msg, elmnts = elmnts)
         con.close()

@app.route('/graficos', methods = ['POST', 'GET'])
def graficos():
   with sql.connect("database.db") as con:
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("SELECT * FROM reports")
         rows = cur.fetchall()
         return render_template("graficos.html", rows = rows)
         con.close()

if __name__ == '__main__':
    app.run(debug=True)
