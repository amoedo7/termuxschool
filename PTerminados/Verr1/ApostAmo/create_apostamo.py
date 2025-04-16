import os
import shutil

def create_project_structure():
    # Definir directorios base
    directories = [
        'src',
        'templates',
        'static',
        'logs',
        'data',
        'config'
    ]
    
    # Crear directorios
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
    # Crear __init__.py en src para que sea un módulo Python
    with open('src/__init__.py', 'w') as f:
        f.write('')
        
    # Crear archivos básicos
    create_server_file()
    create_database_file()
    create_templates()
    create_static_files()

def create_server_file():
    server_content = '''
from flask import Flask, render_template, request, jsonify
from src.database import Database  # Importación actualizada
import uuid
from datetime import datetime

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_bet():
    if request.method == 'POST':
        data = request.get_json()
        bet_id = str(uuid.uuid4())
        db.create_bet(
            bet_id,
            data['question'],
            data['option_a'],
            data['option_b'],
            data['end_time']
        )
        return jsonify({'bet_id': bet_id})
    return render_template('create.html')

@app.route('/bet/<bet_id>')
def join_bet(bet_id):
    bet = db.get_bet(bet_id)
    if bet:
        return render_template('bet.html', bet=bet)
    return "Apuesta no encontrada", 404

@app.route('/bet/<bet_id>/place', methods=['POST'])
def place_bet(bet_id):
    data = request.get_json()
    user_id = request.remote_addr
    success = db.place_bet(bet_id, data['side'], int(data['amount']), user_id)
    if success:
        bet = db.get_bet(bet_id)
        return jsonify({
            'total_a': bet['total_a'],
            'total_b': bet['total_b']
        })
    return "Error al realizar la apuesta", 400

@app.route('/bet/<bet_id>/result')
def show_result(bet_id):
    bet = db.get_bet(bet_id)
    if bet and bet['status'] == 'finished':
        return render_template('result.html', bet=bet)
    return "Resultados no disponibles", 404

if __name__ == '__main__':
    app.run(debug=True)
'''
    with open('server.py', 'w') as f:
        f.write(server_content)

def create_database_file():
    database_content = '''
class Database:
    def __init__(self):
        self.bets = {}
        
    def create_bet(self, bet_id, question, option_a, option_b, end_time):
        self.bets[bet_id] = {
            'question': question,
            'option_a': option_a,
            'option_b': option_b,
            'end_time': end_time,
            'side_a': [],
            'side_b': [],
            'total_a': 0,
            'total_b': 0,
            'status': 'active',
            'winner': None,
            'winners': []
        }
        
    def get_bet(self, bet_id):
        return self.bets.get(bet_id)
        
    def place_bet(self, bet_id, side, amount, user_id):
        if bet_id not in self.bets:
            return False
            
        bet = self.bets[bet_id]
        if bet['status'] != 'active':
            return False
            
        if side == 'a':
            bet['side_a'].append({'user_id': user_id, 'amount': amount})
            bet['total_a'] += amount
        else:
            bet['side_b'].append({'user_id': user_id, 'amount': amount})
            bet['total_b'] += amount
        
        self._update_matchings(bet_id)
        return True
    
    def _update_matchings(self, bet_id):
        bet = self.bets[bet_id]
        min_total = min(bet['total_a'], bet['total_b'])
        
        # Actualizar las apuestas emparejadas
        matched_a = []
        matched_b = []
        current_total = 0
        
        for bet_a in sorted(bet['side_a'], key=lambda x: x['amount']):
            if current_total + bet_a['amount'] <= min_total:
                matched_a.append(bet_a)
                current_total += bet_a['amount']
        
        current_total = 0
        for bet_b in sorted(bet['side_b'], key=lambda x: x['amount']):
            if current_total + bet_b['amount'] <= min_total:
                matched_b.append(bet_b)
                current_total += bet_b['amount']
        
        bet['matched_a'] = matched_a
        bet['matched_b'] = matched_b
'''
    with open('src/database.py', 'w') as f:
        f.write(database_content)

def create_static_files():
    # styles.css
    css_content = '''
:root {
    --primary-color: #4CAF50;
    --secondary-color: #2196F3;
    --background-color: #f5f5f5;
    --text-color: #333;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    background-color: var(--background-color);
    color: var(--text-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.btn-primary {
    display: inline-block;
    padding: 10px 20px;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-primary:hover {
    background-color: #45a049;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.bet-status {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
}

.side-a,
.side-b {
    flex: 1;
    padding: 20px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 0 10px;
}
'''

    # script.js
    js_content = '''
document.addEventListener('DOMContentLoaded', function() {
    // Formulario de creación de apuesta
    const createBetForm = document.getElementById('createBetForm');
    if (createBetForm) {
        createBetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                question: document.getElementById('question').value,
                option_a: document.getElementById('option_a').value,
                option_b: document.getElementById('option_b').value,
                end_time: document.getElementById('end_time').value
            };

            try {
                const response = await fetch('/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                window.location.href = `/bet/${data.bet_id}`;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Formulario para realizar apuesta
    const placeBetForm = document.getElementById('placeBetForm');
    if (placeBetForm) {
        placeBetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                side: document.getElementById('bet_side').value,
                amount: document.getElementById('bet_amount').value
            };

            try {
                const betId = window.location.pathname.split('/').pop();
                const response = await fetch(`/bet/${betId}/place`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                updateBetStatus(data);
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});

function updateBetStatus(data) {
    const totalA = document.getElementById('total-a');
    const totalB = document.getElementById('total-b');
    if (totalA) totalA.textContent = data.total_a;
    if (totalB) totalB.textContent = data.total_b;
}
'''

    # Crear los archivos
    with open('static/styles.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

def create_templates():
    # index.html
    index_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApostAmo - Apuestas Personalizadas</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <h1>Bienvenido a ApostAmo</h1>
        <p>Crea tus propias apuestas y comparte con amigos</p>
        <a href="/create" class="btn-primary">Crear Nueva Apuesta</a>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
'''

    # create.html
    create_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crear Apuesta - ApostAmo</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <h2>Crear Nueva Apuesta</h2>
        <form id="createBetForm">
            <div class="form-group">
                <label for="question">Pregunta de la apuesta:</label>
                <input type="text" id="question" required>
            </div>
            <div class="form-group">
                <label for="option_a">Opción A:</label>
                <input type="text" id="option_a" required>
            </div>
            <div class="form-group">
                <label for="option_b">Opción B:</label>
                <input type="text" id="option_b" required>
            </div>
            <div class="form-group">
                <label for="end_time">Fecha de finalización:</label>
                <input type="datetime-local" id="end_time" required>
            </div>
            <button type="submit" class="btn-primary">Crear Apuesta</button>
        </form>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
'''

    # bet.html
    bet_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Participar en Apuesta - ApostAmo</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <div class="bet-info">
            <h2>{{ bet.question }}</h2>
            <div class="bet-status">
                <div class="side-a">
                    <h3>{{ bet.option_a }}</h3>
                    <p>Total: <span id="total-a">{{ bet.total_a }}</span> 💎</p>
                </div>
                <div class="side-b">
                    <h3>{{ bet.option_b }}</h3>
                    <p>Total: <span id="total-b">{{ bet.total_b }}</span> 💎</p>
                </div>
            </div>
        </div>
        <form id="placeBetForm">
            <div class="form-group">
                <label>Elige tu lado:</label>
                <select id="bet_side" required>
                    <option value="a">{{ bet.option_a }}</option>
                    <option value="b">{{ bet.option_b }}</option>
                </select>
            </div>
            <div class="form-group">
                <label>Cantidad de diamantes:</label>
                <input type="number" id="bet_amount" min="1" required>
            </div>
            <button type="submit" class="btn-primary">Apostar</button>
        </form>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
'''

    # result.html
    result_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados - ApostAmo</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <h2>Resultados de la Apuesta</h2>
        <div class="results">
            <h3>{{ bet.question }}</h3>
            <div class="winner-section">
                <h4>Lado Ganador: {{ bet.winner }}</h4>
                <p>Total apostado: {{ bet.total_winner }} 💎</p>
            </div>
            <div class="distributions">
                <h4>Distribución de Ganancias</h4>
                <ul id="winners-list">
                    {% for winner in bet.winners %}
                    <li>
                        {{ winner.user_id }}: {{ winner.earnings }} 💎
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
'''

    # Crear los archivos
    templates = {
        'index.html': index_content,
        'create.html': create_content,
        'bet.html': bet_content,
        'result.html': result_content
    }

    for filename, content in templates.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    create_project_structure()
    print("¡Estructura del proyecto ApostAmo creada exitosamente!")
