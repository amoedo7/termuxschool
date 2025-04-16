import hashlib
import secrets
import time
import sqlite3
import json
from datetime import datetime, timedelta
import threading
import os

class Database:
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()

    def __init__(self):
        self.db_path = 'apostamo.db'
        self._init_database()
        # Eliminamos self.bets, self.users y self.finished_bets ya que todo estará en SQLite
        
    def _init_database(self):
        """Initialize the database with required tables and admin user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    diamonds INTEGER DEFAULT 1000,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS bets (
                    id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    total_a INTEGER DEFAULT 0,
                    total_b INTEGER DEFAULT 0,
                    creator TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    judge_token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    winner TEXT,
                    finished_at TIMESTAMP,
                    FOREIGN KEY (creator) REFERENCES users (username)
                );

                CREATE TABLE IF NOT EXISTS bet_participants (
                    bet_id TEXT,
                    username TEXT,
                    amount INTEGER,
                    side TEXT,
                    participated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (bet_id) REFERENCES bets (id),
                    FOREIGN KEY (username) REFERENCES users (username),
                    PRIMARY KEY (bet_id, username, participated_at)
                );
            """)
            conn.commit()

            # Crear usuario admin por defecto
            try:
                admin_password = hashlib.sha256('admin'.encode()).hexdigest()
                cursor.execute("""
                    INSERT OR IGNORE INTO users (username, password, diamonds, created_at)
                    VALUES (?, ?, 1000, datetime('now'))
                """, ('admin', admin_password))
                conn.commit()
            except Exception as e:
                print(f"Error creating admin user: {e}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection

    def create_bet(self, question, option_a, option_b, creator):
        try:
            bet_id = secrets.token_hex(4)
            judge_token = secrets.token_hex(8)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO bets (
                        id, question, option_a, option_b, 
                        total_a, total_b, creator, status, 
                        judge_token, created_at
                    ) VALUES (?, ?, ?, ?, 0, 0, ?, 'active', ?, datetime('now'))
                """, (bet_id, question, option_a, option_b, creator, judge_token))
                conn.commit()
                return bet_id
        except Exception as e:
            print(f"Error creating bet: {e}")
            return None

    def place_bet(self, bet_id, side, amount, username):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar si el usuario existe y tiene suficientes diamantes
                cursor.execute("SELECT diamonds FROM users WHERE username = ?", (username,))
                user_result = cursor.fetchone()
                
                if not user_result:
                    return False, "Usuario no encontrado"
                
                current_diamonds = user_result[0]
                if current_diamonds < amount:
                    return False, "No tienes suficientes diamantes"

                # Verificar si la apuesta existe y está activa
                cursor.execute("SELECT status FROM bets WHERE id = ?", (bet_id,))
                bet_result = cursor.fetchone()
                
                if not bet_result:
                    return False, "Apuesta no encontrada"
                if bet_result[0] != 'active':
                    return False, "Esta apuesta ya no está activa"

                # Verificar si el usuario ya ha apostado en cualquier lado de esta apuesta
                cursor.execute("""
                    SELECT side FROM bet_participants 
                    WHERE bet_id = ? AND username = ?
                """, (bet_id, username))
                existing_bet = cursor.fetchone()
                
                if existing_bet:
                    return False, "Ya has participado en esta apuesta. No puedes apostar en ambos lados."

                # Iniciar transacción
                cursor.execute("BEGIN TRANSACTION")
                try:
                    # Actualizar el balance del usuario
                    cursor.execute("""
                        UPDATE users 
                        SET diamonds = diamonds - ? 
                        WHERE username = ?
                    """, (amount, username))

                    # Actualizar los totales de la apuesta
                    if side == 'a':
                        cursor.execute("""
                            UPDATE bets 
                            SET total_a = total_a + ? 
                            WHERE id = ?
                        """, (amount, bet_id))
                    else:
                        cursor.execute("""
                            UPDATE bets 
                            SET total_b = total_b + ? 
                            WHERE id = ?
                        """, (amount, bet_id))

                    # Registrar la participación en la apuesta
                    cursor.execute("""
                        INSERT INTO bet_participants (
                            bet_id, username, amount, side, 
                            participated_at
                        ) VALUES (?, ?, ?, ?, datetime('now'))
                    """, (bet_id, username, amount, side))

                    conn.commit()
                    return True, "Apuesta realizada con éxito"
                except Exception as e:
                    conn.rollback()
                    print(f"Error en transacción: {e}")
                    return False, "Error en la transacción"
        except Exception as e:
            print(f"Error en place_bet: {e}")
            return False, str(e)

    def get_all_bets(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, question, option_a, option_b, 
                           total_a, total_b, creator, status, 
                           created_at 
                    FROM bets 
                    ORDER BY created_at DESC
                """)
                bets = cursor.fetchall()
                return [{
                    'id': bet[0],
                    'question': bet[1],
                    'option_a': bet[2],
                    'option_b': bet[3],
                    'total_a': bet[4],
                    'total_b': bet[5],
                    'creator': bet[6],
                    'status': bet[7],
                    'created_at': bet[8]
                } for bet in bets]
        except Exception as e:
            print(f"Error getting bets: {e}")
            return []

    def verify_judge(self, bet_id, token):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT judge_token FROM bets 
        WHERE id = ? AND judge_token = ?
        ''', (bet_id, token))
        result = cursor.fetchone()
        return result is not None
    
    def finalize_bet(self, bet_id, winning_side):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener la apuesta y verificar estado
                cursor.execute("SELECT * FROM bets WHERE id = ? AND status = 'active'", (bet_id,))
                bet = cursor.fetchone()
                
                if not bet:
                    return False, "Apuesta no disponible o ya finalizada"
                
                # Obtener todos los participantes ordenados por tiempo
                cursor.execute("""
                    SELECT username, amount, side, participated_at 
                    FROM bet_participants 
                    WHERE bet_id = ? 
                    ORDER BY participated_at ASC
                """, (bet_id,))
                participants = cursor.fetchall()
                
                # Separar y ordenar participantes por lado
                side_a = [dict(p) for p in participants if p['side'] == 'a']
                side_b = [dict(p) for p in participants if p['side'] == 'b']
                
                # Calcular totales por lado
                total_a = sum(p['amount'] for p in side_a)
                total_b = sum(p['amount'] for p in side_b)
                
                cursor.execute("BEGIN TRANSACTION")
                try:
                    # Procesar lado ganador
                    if winning_side == 'a':
                        winning_bets = side_a
                        losing_bets = side_b
                        winning_total = total_a
                        losing_total = total_b
                    else:
                        winning_bets = side_b
                        losing_bets = side_a
                        winning_total = total_b
                        losing_total = total_a

                    # Procesar cada apuesta ganadora en orden
                    available_pool = losing_total  # Pool disponible para pagar
                    for bet in winning_bets:
                        if available_pool <= 0:
                            # Si no hay más pool, devolver la apuesta original
                            refund = bet['amount']
                        else:
                            # Calcular cuánto puede ganar de lo disponible
                            possible_win = min(bet['amount'], available_pool)
                            refund = bet['amount']  # Devolver apuesta original
                            earnings = possible_win  # Más las ganancias disponibles
                            available_pool -= possible_win
                            
                            # Actualizar balance del usuario
                            cursor.execute("""
                                UPDATE users 
                                SET diamonds = diamonds + ? 
                                WHERE username = ?
                            """, (refund + earnings, bet['username']))

                    # Marcar la apuesta como finalizada
                    cursor.execute("""
                        UPDATE bets 
                        SET status = 'finished',
                            winner = ?,
                            finished_at = datetime('now')
                        WHERE id = ?
                    """, (winning_side, bet_id))
                    
                    conn.commit()
                    return True, "Apuesta finalizada exitosamente"
                    
                except Exception as e:
                    conn.rollback()
                    print(f"Error en finalize_bet transaction: {e}")
                    return False, str(e)
                
        except Exception as e:
            print(f"Error en finalize_bet: {e}")
            return False, str(e)
    
    def _clean_expired_bets(self):
        current_time = time.time()
        expired_bets = [
            bet_id for bet_id, data in self.finished_bets.items()
            if current_time > data['expire_time']
        ]
        for bet_id in expired_bets:
            del self.finished_bets[bet_id]
    
    def get_bet_result(self, bet_id, username=None):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener información de la apuesta
                cursor.execute("""
                    SELECT * FROM bets WHERE id = ?
                """, (bet_id,))
                bet = cursor.fetchone()
                
                if not bet:
                    return None
                    
                bet_dict = dict(bet)
                
                # Obtener todos los participantes
                cursor.execute("""
                    SELECT username, amount, side 
                    FROM bet_participants 
                    WHERE bet_id = ?
                    ORDER BY amount DESC
                """, (bet_id,))
                participants = cursor.fetchall()
                
                # Separar participantes por lado
                bet_dict['side_a'] = [dict(p) for p in participants if p['side'] == 'a']
                bet_dict['side_b'] = [dict(p) for p in participants if p['side'] == 'b']
                
                # Si se proporciona un username, obtener su apuesta específica
                if username:
                    cursor.execute("""
                        SELECT amount, side 
                        FROM bet_participants 
                        WHERE bet_id = ? AND username = ?
                    """, (bet_id, username))
                    user_bet = cursor.fetchone()
                    if user_bet:
                        bet_dict['user_bet'] = dict(user_bet)
                
                return bet_dict
        except Exception as e:
            print(f"Error getting bet result: {e}")
            return None
    
    def get_user_bets(self, username):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener apuestas activas donde el usuario participó
                cursor.execute("""
                    SELECT DISTINCT b.* 
                    FROM bets b
                    JOIN bet_participants bp ON b.id = bp.bet_id
                    WHERE bp.username = ? AND b.status = 'active'
                    ORDER BY b.created_at DESC
                """, (username,))
                active_bets = [dict(row) for row in cursor.fetchall()]
                
                # Obtener apuestas finalizadas donde el usuario participó
                cursor.execute("""
                    SELECT DISTINCT b.* 
                    FROM bets b
                    JOIN bet_participants bp ON b.id = bp.bet_id
                    WHERE bp.username = ? AND b.status = 'finished'
                    ORDER BY b.finished_at DESC
                """, (username,))
                finished_bets = [dict(row) for row in cursor.fetchall()]
                
                return {
                    'active': active_bets,
                    'finished': finished_bets
                }
        except Exception as e:
            print(f"Error getting user bets: {e}")
            return {'active': [], 'finished': []}
        
    def get_bet(self, bet_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Obtener la información de la apuesta
                cursor.execute("""
                    SELECT * FROM bets WHERE id = ?
                """, (bet_id,))
                bet = cursor.fetchone()
                
                if not bet:
                    return None
                    
                # Obtener los participantes
                cursor.execute("""
                    SELECT username, amount, side 
                    FROM bet_participants 
                    WHERE bet_id = ?
                """, (bet_id,))
                participants = cursor.fetchall()
                
                # Convertir a diccionario y agregar participantes
                bet_dict = dict(bet)
                bet_dict['side_a'] = [
                    {'user_id': p['username'], 'amount': p['amount']} 
                    for p in participants if p['side'] == 'a'
                ]
                bet_dict['side_b'] = [
                    {'user_id': p['username'], 'amount': p['amount']} 
                    for p in participants if p['side'] == 'b'
                ]
                
                return bet_dict
        except Exception as e:
            print(f"Error getting bet: {e}")
            return None

    def _format_bet(self, bet_dict, participants):
        return {
            'id': bet_dict['id'],
            'question': bet_dict['question'],
            'option_a': bet_dict['option_a'],
            'option_b': bet_dict['option_b'],
            'total_a': bet_dict['total_a'],
            'total_b': bet_dict['total_b'],
            'status': bet_dict['status'],
            'winner': bet_dict['winner'],
            'judge_token': bet_dict['judge_token'],
            'side_a': [dict(p) for p in participants if p['side'] == 'a'],
            'side_b': [dict(p) for p in participants if p['side'] == 'b'],
            'created_at': bet_dict['created_at'],
            'finished_at': bet_dict['finished_at']
        }
        
    def create_user(self, username, password):
        try:
            # Hash de la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar si el usuario ya existe
                cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return False, "El nombre de usuario ya existe"
                
                # Crear nuevo usuario
                cursor.execute("""
                    INSERT INTO users (username, password, diamonds, created_at)
                    VALUES (?, ?, 1000, datetime('now'))
                """, (username, password_hash))
                conn.commit()
                return True, "Usuario creado exitosamente"
        except Exception as e:
            print(f"Error creating user: {e}")
            return False, str(e)

    def verify_user(self, username, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT username FROM users 
                    WHERE username = ? AND password = ?
                """, (username, password_hash))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False

    def get_user_balance(self, username):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT diamonds FROM users WHERE username = ?", 
                             (username,))
                result = cursor.fetchone()
                if result is None:
                    # Si el usuario no existe, retornar None en lugar de 0
                    return None
                return result['diamonds']
        except Exception as e:
            print(f"Error getting user balance: {e}")
            return None
    
    def add_diamonds(self, username, amount):
        if username not in self.users:
            return False, "Usuario no encontrado"
            
        self.users[username]['diamonds'] += amount
        self.users[username]['transactions'].append({
            'type': 'deposit',
            'amount': amount,
            'timestamp': time.time()
        })
        return True, "Diamantes añadidos correctamente"

    def get_active_bets(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, question, option_a, option_b, 
                           total_a, total_b, creator, created_at 
                    FROM bets 
                    WHERE status = 'active' 
                    ORDER BY created_at DESC
                """)
                bets = cursor.fetchall()
                return [{
                    'id': bet[0],
                    'question': bet[1],
                    'option_a': bet[2],
                    'option_b': bet[3],
                    'total_a': bet[4],
                    'total_b': bet[5],
                    'creator': bet[6],
                    'created_at': bet[7]
                } for bet in bets]
        except Exception as e:
            print(f"Error getting active bets: {e}")
            return []

    def get_top_users(self, limit=20):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT username, diamonds, created_at,
                           (SELECT COUNT(*) FROM bet_participants WHERE username = users.username) as total_bets
                    FROM users 
                    ORDER BY diamonds DESC, total_bets DESC
                    LIMIT ?
                """, (limit,))
                
                users = cursor.fetchall()
                return [{
                    'username': user['username'],
                    'diamonds': user['diamonds'],
                    'total_bets': user['total_bets'],
                    'created_at': user['created_at']
                } for user in users]
        except Exception as e:
            print(f"Error getting top users: {e}")
            return []

    def get_bet_participants(self, bet_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT username, amount, side 
                    FROM bet_participants 
                    WHERE bet_id = ?
                    ORDER BY amount DESC
                """, (bet_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting bet participants: {e}")
            return []
