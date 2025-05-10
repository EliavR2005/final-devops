from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os, time

# Local imports
from encrypt_utils import encrypt_data, decrypt_data
from key_manager import get_encryption_key

# ── CARGA DE .env ──────────────────────────────────────────────────────────────
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ENCRYPT_KEY = get_encryption_key()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not SECRET_KEY or not ENCRYPT_KEY:
    raise RuntimeError("Falta SECRET_KEY o ENCRYPT_KEY en tu .env")

# ── APP & SQLALCHEMY CONFIG ──────────────────────────────────────────────────
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': SECRET_KEY,
    'SESSION_TYPE': 'filesystem',
    'SQLALCHEMY_DATABASE_URI': f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ── MONITORIZACIÓN CON PROMETHEUS ─────────────────────────────────────────────
REQUEST_COUNT = Counter('flask_requests_total', 'Count of requests', ['method','endpoint','http_status'])
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['method','endpoint'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(request.method, request.endpoint or 'none', response.status_code).inc()
    latency = time.time() - getattr(request, 'start_time', time.time())
    REQUEST_LATENCY.labels(request.method, request.endpoint or 'none').observe(latency)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# ── CIFRADO FERNET ────────────────────────────────────────────────────────────
cipher = Fernet(ENCRYPT_KEY)

def safe_decrypt(encrypted_data, field_name="dato"):
    """
    Intenta descifrar un campo cifrado.
    Primero prueba tu función decrypt_data (caso de datos cifrados por encrypt_utils),
    si falla, prueba con Fernet.decrypt (prefijo gAAAAA),
    y si ambos fallan devuelve el texto original.
    """
    try:
        # 1) Intentar decrypt_data (para datos cifrados con encrypt_utils)
        return decrypt_data(encrypted_data)
    except Exception:
        # 2) Si falla, y parece un token Fernet, intentar cipher.decrypt
        if isinstance(encrypted_data, str) and encrypted_data.startswith('gAAAAA'):
            try:
                return cipher.decrypt(encrypted_data.encode()).decode()
            except InvalidToken:
                app.logger.error(f"Error desencriptando {field_name}: token inválido de Fernet")
        # 3) Si todo falla, devolver original
        app.logger.error(f"Error desencriptando {field_name}: no se pudo descifrar con ningún método")
        return encrypted_data

# ── MODELO ORM ─────────────────────────────────────────────────────────────────
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email_encrypted = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    rfc_encrypted = db.Column(db.Text, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    role = db.Column(db.String(10), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── COMANDOS CLI ───────────────────────────────────────────────────────────────

@app.cli.command("encrypt-placeholders")
def encrypt_placeholders():
    users = User.query.all()
    count = 0
    for u in users:
        updated = False
        for attr in ['name','email_encrypted','address','phone','rfc_encrypted']:
            val = getattr(u, attr)
            if not str(val).startswith("gAAAAA"):
                setattr(u, attr, encrypt_data(val))
                updated = True
        if updated:
            count += 1
    db.session.commit()
    print(f"Re‑cifrados {count} usuarios.")

# ── COMANDO CLI PARA CREAR ADMINISTRADOR (COMENTADO) ───────────────────────────
"""
@app.cli.command("create-admin")
def create_admin():
    \"\"\"Crea un usuario administrador automáticamente.\"\"\"
    from werkzeug.security import generate_password_hash

    # Datos del administrador
    username = "Liav"
    password = "admin050430"
    email = "liav@example.com"
    name = "Liav Administrador"
    address = "Av. Principal 123, Ciudad"
    phone = "+52 55 1234 5678"
    rfc = "LIAV050430XYZ"
    birth_date = "2005-04-30"
    gender = "Male"
    role = "admin"

    # Verifica si el usuario ya existe
    existing_user = User.query.filter_by(username=username).first()
    if (existing_user):
        print(f"El usuario '{username}' ya existe.")
        return

    # Crea el usuario administrador
    admin = User(
        username=username,
        password_hash=generate_password_hash(password),
        email_encrypted=cipher.encrypt(email.encode()).decode(),
        name=name,
        address=cipher.encrypt(address.encode()).decode(),
        phone=cipher.encrypt(phone.encode()).decode(),
        rfc_encrypted=cipher.encrypt(rfc.encode()).decode(),
        birth_date=birth_date,
        gender=gender,
        role=role,
    )
    db.session.add(admin)
    db.session.commit()
    print(f"Usuario administrador '{username}' creado con éxito.")
"""

@app.cli.command("clean-encryption")
def clean_encryption():
    """Limpia y re-cifra los datos en la base de datos."""
    users = User.query.all()
    for u in users:
        try:
            u.email_encrypted = encrypt_data(decrypt_data(u.email_encrypted))
            u.address = encrypt_data(decrypt_data(u.address))
            u.phone = encrypt_data(decrypt_data(u.phone))
            u.rfc_encrypted = encrypt_data(decrypt_data(u.rfc_encrypted))
        except InvalidToken:
            app.logger.error(f"Error limpiando datos para el usuario {u.username}")
    db.session.commit()
    print("Datos cifrados limpiados correctamente.")

# ── RUTAS DE AUTENTICACIÓN ─────────────────────────────────────────────────────
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        new_user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password']),
            email_encrypted=cipher.encrypt(data['email'].encode()).decode(),
            name=data['name'],
            address=cipher.encrypt(data['address'].encode()).decode(),
            phone=cipher.encrypt(data['phone'].encode()).decode(),
            rfc_encrypted=cipher.encrypt(data['rfc'].encode()).decode(),
            birth_date=data['birth_date'],
            gender=data['gender'],
            role='client'
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {e}', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('can_view_encrypted', None)  # Elimina el indicador de la sesión
    return redirect(url_for('login'))


# ── RUTAS DE USUARIO ──────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    me = User.query.get(session.get('user_id'))
    admins = User.query.filter(User.role=='admin', User.id!=me.id).all()
    clients = User.query.filter_by(role='client').all()
    return render_template('dashboard.html', me=me, admins=admins, clients=clients)

@app.route('/user/<username>')
@login_required
def view_user(username):
    if current_user.role != 'admin':
        flash('No tienes permiso', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.filter_by(username=username).first_or_404()
    # Mostrar inicialmente los valores cifrados
    data = {
        "email": user.email_encrypted,
        "address": user.address,
        "phone": user.phone,
        "rfc": user.rfc_encrypted,
    }
    return render_template('user_detail.html', user=user, data=data)

@app.route('/user/<username>/edit', methods=['POST'])
@login_required
def edit_user(username):
    if current_user.role != 'admin':
        flash('No tienes permiso para editar', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.filter_by(username=username).first_or_404()
    form = request.form

    # Solo cifra los datos si no están ya cifrados
    user.name = form['name']
    user.email_encrypted = cipher.encrypt(form['email'].encode()).decode() if not form['email'].startswith("gAAAAA") else form['email']
    user.address = cipher.encrypt(form['address'].encode()).decode() if not form['address'].startswith("gAAAAA") else form['address']
    user.phone = cipher.encrypt(form['phone'].encode()).decode() if not form['phone'].startswith("gAAAAA") else form['phone']
    user.rfc_encrypted = cipher.encrypt(form['rfc'].encode()).decode() if not form['rfc'].startswith("gAAAAA") else form['rfc']
    user.birth_date = form['birth_date']
    user.gender = form['gender']

    db.session.commit()
    flash('Usuario actualizado', 'success')
    return redirect(url_for('view_user', username=username))

@app.route('/user/<username>/encrypted', methods=['POST'])
@login_required
def view_user_encrypted(username):
    user = User.query.filter_by(username=username).first_or_404()

    if current_user.role.lower() != 'admin':
        return jsonify({'error': 'Acceso no autorizado'}), 403

    data = request.get_json() or {}
    if not current_user.check_password(data.get('admin_password', '')):
        return jsonify({'error': 'Contraseña incorrecta'}), 403

    try:
        # Devuelve los campos ya descifrados para que el JS los muestre
        return jsonify({
            "email":   safe_decrypt(user.email_encrypted, "Email"),
            "address": safe_decrypt(user.address,       "Dirección"),
            "phone":   safe_decrypt(user.phone,         "Teléfono"),
            "rfc":     safe_decrypt(user.rfc_encrypted, "RFC"),
        })
    except Exception as e:
        return jsonify({'error': 'Error al descifrar', 'details': str(e)}), 500

# ── EJECUCIÓN ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")

print(generate_password_hash("admin050430"))

