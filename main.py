from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal
@app.route('/')
def index():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo, concluida FROM tarefas')
    tarefas = cursor.fetchall()
    pendentes = [t for t in tarefas if t[2] == 0]
    concluidas = [t for t in tarefas if t[2] == 1]
    conn.close()
    return render_template('index.html',
                           pendentes=pendentes,
                           concluidas=concluidas,
                           total_pendentes=len(pendentes),
                           total_concluidas=len(concluidas))

# Adiciona nova tarefa
@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form['titulo']
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (titulo) VALUES (?)', (titulo,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Concluir tarefa
@app.route('/concluir/<int:id>')
def concluir(id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET concluida = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Remover tarefa individual
@app.route('/remover/<int:id>')
def remover(id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Remover todas as tarefas
@app.route('/remover_todas')
def remover_todas():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Editar tarefa
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    novo_titulo = request.form['novo_titulo']
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET titulo = ? WHERE id = ?', (novo_titulo, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
