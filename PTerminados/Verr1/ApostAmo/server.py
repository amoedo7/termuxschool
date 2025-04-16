# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from src.database import Database
import uuid
from datetime import datetime
import secrets
from functools import wraps
import os
import time

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar en producción

def init_app():
    # Esperar a que cualquier proceso anterior libere la base de datos
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            if os.path.exists('apostamo.db'):
                os.remove('apostamo.db')
            break
        except PermissionError:
            if attempt < max_attempts - 1:
                print(f"Intento {attempt + 1} de {max_attempts} para eliminar la base de datos...")
                time.sleep(2)
            else:
                print("No se pudo eliminar la base de datos, continuando con la existente...")

    # Inicializar la base de datos
    return Database.get_instance()

# Inicializar la base de datos
db = init_app()

# Middleware para verificar autenticación
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Decorator modificado para añadir datos de usuario
def with_user_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_balance = 0
        if 'username' in session:
            try:
                user_balance = db.get_user_balance(session['username'])
                # Si el balance es None o 0, el usuario probablemente no existe
                if user_balance is None:
                    session.clear()
                    return redirect(url_for('login'))
            except Exception as e:
                print(f"Error getting user balance: {e}")
                session.clear()
                return redirect(url_for('login'))
        return f(*args, user_balance=user_balance, **kwargs)
    return decorated_function

@app.route('/')
@with_user_data
def index(user_balance=None):
    # Obtener todas las apuestas activas
    active_bets = db.get_active_bets()
    print("Apuestas activas:", active_bets)  # Debug log
    return render_template('index.html', 
                         active_bets=active_bets,
                         user_balance=user_balance)

@app.route('/create', methods=['GET', 'POST'])
@login_required
@with_user_data
def create_bet(user_balance=None):
    if request.method == 'GET':
        return render_template('create.html', user_balance=user_balance)
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400

        required_fields = ['question', 'optionA', 'optionB']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Faltan campos requeridos'}), 400

        bet_id = db.create_bet(
            data['question'],
            data['optionA'],
            data['optionB'],
            session['username']
        )

        if bet_id:
            return jsonify({
                'success': True,
                'bet_id': bet_id,
                'message': 'Apuesta creada exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al crear la apuesta'
            }), 500
    except Exception as e:
        print(f"Error en create_bet: {e}")
        return jsonify({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }), 500

@app.route('/bet/<bet_id>/links')
@with_user_data
def show_links(bet_id, user_balance=None):
    bet = db.get_bet(bet_id)
    if not bet:
        return "Apuesta no encontrada", 404
    
    urls = {
        'bet_url': f"{request.host_url}bet/{bet_id}",
        'judge_url': f"{request.host_url}bet/{bet_id}/judge/{bet['judge_token']}"
    }
    return render_template('links.html', urls=urls, bet=bet, user_balance=user_balance)

@app.route('/bet/<bet_id>')
@with_user_data
def join_bet(bet_id, user_balance=None):
    bet = db.get_bet(bet_id)
    if not bet:
        return "Apuesta no encontrada", 404
    
    # Pasar el estado de autenticación a la plantilla
    is_authenticated = 'username' in session
    return render_template('bet.html', 
                         bet=bet, 
                         is_authenticated=is_authenticated,
                         user_balance=user_balance)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        success, message = db.create_user(data['username'], data['password'])
        if success:
            session['username'] = data['username']
            return jsonify({
                'success': True,
                'message': '¡Registro exitoso!',
                'username': data['username'],
                'balance': 1000
            })
        return jsonify({'success': False, 'message': message})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if db.verify_user(data['username'], data['password']):
            session['username'] = data['username']
            balance = db.get_user_balance(data['username'])
            return jsonify({
                'success': True,
                'message': f'¡Bienvenido, {data["username"]}!',
                'username': data['username'],
                'balance': balance
            })
        return jsonify({'success': False, 'message': 'Credenciales inválidas'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile')
@with_user_data
def profile(user_balance=None):
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', 
                         username=session['username'],
                         user_balance=user_balance)

@app.route('/add-diamonds', methods=['POST'])
@login_required
def add_diamonds():
    data = request.get_json()
    amount = int(data['amount'])
    success, message = db.add_diamonds(session['username'], amount)
    return jsonify({'success': success, 'message': message})

@app.route('/bet/<bet_id>/place', methods=['POST'])
@login_required
@with_user_data
def place_bet(bet_id, user_balance=None):
    try:
        data = request.get_json()
        success, message = db.place_bet(bet_id, data['side'], data['amount'], session['username'])

        if success:
            bet = db.get_bet(bet_id)
            new_balance = db.get_user_balance(session['username'])
            
            # Calcular estadísticas adicionales
            side_a_participants = len(bet['side_a'])
            side_b_participants = len(bet['side_b'])
            
            return jsonify({
                'success': True,
                'message': message,
                'total_a': bet['total_a'],
                'total_b': bet['total_b'],
                'new_balance': new_balance,
                'side_a_count': side_a_participants,
                'side_b_count': side_b_participants,
                'side_a_average': round(bet['total_a'] / side_a_participants if side_a_participants > 0 else 0, 1),
                'side_b_average': round(bet['total_b'] / side_b_participants if side_b_participants > 0 else 0, 1)
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    except Exception as e:
        print(f"Error en place_bet: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/bet/<bet_id>/judge/<token>')
def judge_bet(bet_id, token):
    try:
        # Verificar token del juez
        if not db.verify_judge(bet_id, token):
            return render_template('error.html', 
                message="Acceso denegado. Token de juez inválido.")
        
        # Obtener información de la apuesta
        bet = db.get_bet(bet_id)
        if not bet:
            return render_template('error.html', 
                message="Apuesta no encontrada")
            
        if bet['status'] != 'active':
            return render_template('error.html', 
                message="Esta apuesta ya ha sido finalizada")
        
        return render_template('judge.html', bet=bet, token=token)
    except Exception as e:
        print(f"Error en judge_bet: {e}")
        return render_template('error.html', 
            message="Error al cargar la página del juez")

@app.route('/judge/<bet_id>/<token>/decide', methods=['POST'])
def judge_decide(bet_id, token):
    if not db.verify_judge(bet_id, token):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    data = request.get_json()
    winning_side = data.get('winner')
    if winning_side not in ['a', 'b']:
        return jsonify({'error': 'Opción inválida'}), 400
    
    success = db.finalize_bet(bet_id, winning_side)
    if success:
        return jsonify({'success': True, 'redirect': f'/bet/{bet_id}/result'})
    return jsonify({'error': 'Error al finalizar la apuesta'}), 400

@app.route('/bet/<bet_id>/result')
@with_user_data
def show_result(bet_id, user_balance=None):
    try:
        # Obtener resultado con la apuesta del usuario si está autenticado
        username = session.get('username')
        bet = db.get_bet_result(bet_id, username)
        
        if not bet:
            return render_template('error.html', 
                                 message="Apuesta no encontrada",
                                 user_balance=user_balance)
        
        return render_template('result.html', 
                             bet=bet,
                             user_balance=user_balance)
    except Exception as e:
        print(f"Error mostrando resultados: {e}")
        return render_template('error.html', 
                             message="Error al cargar los resultados",
                             user_balance=user_balance)

@app.route('/ranking')
@with_user_data
def ranking(user_balance=None):
    top_users = db.get_top_users(limit=20)  # Obtener top 20 usuarios
    return render_template('ranking.html', 
                         users=top_users,
                         user_balance=user_balance)

@app.route('/quick-auth', methods=['POST'])
def quick_auth():
    data = request.get_json()
    username = data['username']
    password = data['password']
    action = data['action']  # 'login' o 'register'
    
    if action == 'register':
        success, message = db.create_user(username, password)
        if success:
            session['username'] = username
            return jsonify({'success': True, 'balance': 1000})
        return jsonify({'success': False, 'message': message})
    else:  # login
        if db.verify_user(username, password):
            session['username'] = username
            balance = db.get_user_balance(username)
            return jsonify({'success': True, 'balance': balance})
        return jsonify({'success': False, 'message': 'Credenciales inválidas'})

@app.route('/profile/bets')
@login_required
@with_user_data
def user_bets(user_balance=None):
    bets = db.get_user_bets(session['username'])
    return render_template('user_bets.html', bets=bets, user_balance=user_balance)

@app.before_request
def check_user_session():
    """Verificar que el usuario en sesión existe en la base de datos"""
    if 'username' in session:
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM users WHERE username = ?", 
                             (session['username'],))
                user = cursor.fetchone()
                
                # Si el usuario no existe en la DB pero está en sesión
                if not user:
                    # Limpiar la sesión
                    session.clear()
                    return redirect(url_for('login'))
        except Exception as e:
            print(f"Error verificando sesión: {e}")
            session.clear()

if __name__ == '__main__':
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Cambiamos a False para evitar la recarga automática
            use_reloader=False
        )
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
