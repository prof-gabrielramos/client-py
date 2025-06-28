import datetime
import json
import logging
import os
import sqlite3
import requests  # Movido para o topo

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash

from android_sms_gateway.client import AndroidSmsGatewayClient

app = Flask(__name__)
app.secret_key = os.urandom(24)
Bootstrap(app)

# Configuration
CONFIG_DIR = os.path.expanduser("~/.sms-gateway-web")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DB_FILE = os.path.join(CONFIG_DIR, "database.db")
APP_VERSION = "1.0.0"

# Default configuration
DEFAULT_CONFIG = {
    "gateway_url": "http://192.168.1.100:8080",
    "api_key": "",
    "device_id": "web-client",
    "verify_ssl": False,
    "default_country_code": "+55",
    "messages_per_page": 25,
    "auto_refresh_dashboard": True,
    "require_auth": False,
    "username": "admin",
    "password_hash": "",
    "session_timeout": 30,  # minutes
}

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)


# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Merge with default config to ensure all keys exist
                return {**DEFAULT_CONFIG, **config}
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG


# Save configuration
def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving config: {e}")
        return False


# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Messages table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            message TEXT,
            recipients TEXT,
            state TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """
    )

    # Contacts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT UNIQUE,
            group_name TEXT,
            notes TEXT
        )
    """
    )

    # Webhooks table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            events TEXT,
            headers TEXT,
            enabled INTEGER
        )
    """
    )

    conn.commit()
    conn.close()


# Initialize app
config = load_config()
init_db()


# SMS Gateway Client
def get_sms_client():
    return AndroidSmsGatewayClient(
        base_url=config["gateway_url"],
        api_key=config["api_key"] if config["api_key"] else None,
        device_id=config["device_id"],
        verify_ssl=config["verify_ssl"],
    )


# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if config["require_auth"] and "user" not in session:
            flash("Por favor, faça login para acessar esta página.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == config["username"] and check_password_hash(
            config["password_hash"], password
        ):
            session["user"] = username
            session["login_time"] = datetime.datetime.now().isoformat()
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas. Tente novamente.", "error")
            return redirect(url_for("login"))

    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("login_time", None)
    flash("Você foi desconectado.", "info")
    return redirect(url_for("login"))


# Dashboard
@app.route("/")
@login_required
def dashboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get message stats
    cursor.execute("SELECT state, COUNT(*) FROM messages GROUP BY state")
    stats_data = cursor.fetchall()
    stats = {state: count for state, count in stats_data}

    # Get recent messages (last 10)
    cursor.execute(
        "SELECT id, message, recipients, state, created_at FROM messages ORDER BY created_at DESC LIMIT 10"
    )
    recent_messages = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html", stats=stats, recent_messages=recent_messages
    )


# Send SMS page
@app.route("/send", methods=["GET", "POST"])
@login_required
def send_page():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM contacts ORDER BY name")
    contacts = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        data = request.get_json()
        message = data.get("message")
        phone_numbers = data.get("phone_numbers", [])
        with_delivery_report = data.get("with_delivery_report", False)
        sim_number = data.get("sim_number")
        ttl = data.get("ttl")

        # Format phone numbers with default country code if needed
        formatted_numbers = []
        country_code = config.get("default_country_code", "+55")
        for number in phone_numbers:
            number = number.strip()
            if number and not number.startswith("+"):
                if not number.startswith(country_code):
                    number = country_code + number.lstrip("0")
                formatted_numbers.append(number)
            elif number:
                formatted_numbers.append(number)

        if not formatted_numbers:
            return jsonify({"error": "Nenhum número de telefone fornecido"}), 400

        try:
            client = get_sms_client()
            options = {"with_delivery_report": with_delivery_report}
            if sim_number:
                options["sim_number"] = int(sim_number)
            if ttl:
                options["ttl"] = int(ttl)

            response = client.send_sms(formatted_numbers, message, **options)

            # Store message in database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO messages (id, message, recipients, state, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    response.id,
                    message,
                    json.dumps(formatted_numbers),
                    response.state,
                    now,
                    now,
                ),
            )
            conn.commit()
            conn.close()

            return jsonify(
                {
                    "id": response.id,
                    "state": response.state,
                    "recipients": formatted_numbers,
                }
            )
        except Exception as e:
            logging.error(f"Error sending SMS: {e}")
            return jsonify({"error": str(e)}), 500

    return render_template("send.html", contacts=contacts)


# Messages page
@app.route("/messages")
@login_required
def messages():
    page = int(request.args.get("page", 1))
    per_page = config.get("messages_per_page", 25)
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    total_pages = (total_messages + per_page - 1) // per_page

    cursor.execute(
        "SELECT id, message, recipients, state, created_at FROM messages ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (per_page, offset),
    )
    messages_data = cursor.fetchall()

    start_index = offset + 1
    end_index = min(offset + per_page, total_messages)

    conn.close()

    return render_template(
        "messages.html",
        messages=messages_data,
        current_page=page,
        total_pages=total_pages,
        start_index=start_index,
        end_index=end_index,
        total_messages=total_messages,
    )


# Contacts page
@app.route("/contacts", methods=["GET", "POST"])
@login_required
def contacts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if request.method == "POST":
        action = request.args.get("action", "add")
        data = request.get_json()

        if action == "add":
            name = data.get("name")
            phone = data.get("phone")
            group = data.get("group", "")
            notes = data.get("notes", "")

            try:
                cursor.execute(
                    "INSERT INTO contacts (name, phone, group_name, notes) VALUES (?, ?, ?, ?)",
                    (name, phone, group, notes),
                )
                conn.commit()
                return jsonify({"success": True, "id": cursor.lastrowid})
            except sqlite3.IntegrityError:
                return (
                    jsonify({"error": "Este número de telefone já está registrado"}),
                    400,
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()

        elif action == "edit":
            contact_id = request.args.get("id")
            name = data.get("name")
            phone = data.get("phone")
            group = data.get("group", "")
            notes = data.get("notes", "")

            try:
                cursor.execute(
                    "UPDATE contacts SET name = ?, phone = ?, group_name = ?, notes = ? WHERE id = ?",
                    (name, phone, group, notes, contact_id),
                )
                conn.commit()
                return jsonify({"success": True})
            except sqlite3.IntegrityError:
                return (
                    jsonify(
                        {
                            "error": "Este número de telefone já está registrado em outro contato"
                        }
                    ),
                    400,
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()

        elif action == "delete":
            contact_id = request.args.get("id")
            try:
                cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
                conn.commit()
                return jsonify({"success": True})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()

    cursor.execute("SELECT name, phone, group_name, notes FROM contacts ORDER BY name")
    contacts_data = cursor.fetchall()
    conn.close()

    return render_template("contacts.html", contacts=contacts_data)


# Settings page
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    global config

    if request.method == "POST":
        data = request.get_json()
        new_config = config.copy()

        # Update configuration from request
        for key in ["gateway_url", "api_key", "device_id", "default_country_code"]:
            new_config[key] = data.get(key, new_config[key])

        new_config["verify_ssl"] = data.get("verify_ssl", False)
        new_config["messages_per_page"] = data.get("messages_per_page", 25)
        new_config["auto_refresh_dashboard"] = data.get("auto_refresh_dashboard", True)
        new_config["require_auth"] = data.get("require_auth", False)

        auth_changed = False
        if new_config["require_auth"]:
            new_config["username"] = data.get("username", new_config["username"])

            new_password = data.get("new_password", "")
            if new_password:
                current_password = data.get("current_password", "")
                if config["password_hash"] and not check_password_hash(
                    config["password_hash"], current_password
                ):
                    return jsonify({"error": "Senha atual incorreta"}), 400

                new_config["password_hash"] = generate_password_hash(new_password)
                auth_changed = True

        if save_config(new_config):
            config = new_config
            return jsonify({"success": True, "auth_changed": auth_changed})
        else:
            return jsonify({"error": "Falha ao salvar configurações"}), 500

    return render_template("settings.html", settings=config, app_version=APP_VERSION)


# Webhooks page
@app.route("/webhooks", methods=["GET", "POST"])
@login_required
def webhooks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if request.method == "POST":
        action = request.args.get("action", "add")
        data = request.get_json()

        if action == "add":
            name = data.get("name")
            url = data.get("url")
            events = ",".join(data.get("events", []))
            headers = data.get("headers", "{}")
            enabled = data.get("enabled", True)

            try:
                cursor.execute(
                    "INSERT INTO webhooks (name, url, events, headers, enabled) VALUES (?, ?, ?, ?, ?)",
                    (name, url, events, headers, 1 if enabled else 0),
                )
                conn.commit()
                return jsonify({"success": True, "id": cursor.lastrowid})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()

        elif action == "edit":
            webhook_id = request.args.get("id")
            name = data.get("name")
            url = data.get("url")
            events = ",".join(data.get("events", []))
            headers = data.get("headers", "{}")
            enabled = data.get("enabled", True)

            try:
                cursor.execute(
                    "UPDATE webhooks SET name = ?, url = ?, events = ?, headers = ?, enabled = ? WHERE id = ?",
                    (name, url, events, headers, 1 if enabled else 0, webhook_id),
                )
                conn.commit()
                return jsonify({"success": True})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()

        elif action == "delete":
            webhook_id = request.args.get("id")
            try:
                cursor.execute("DELETE FROM webhooks WHERE id = ?", (webhook_id,))
                conn.commit()
                return jsonify({"success": True})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()

        elif action == "test":
            webhook_id = request.args.get("id")
            event_type = data.get("event", "message.sent")

            try:
                cursor.execute(
                    "SELECT url, headers FROM webhooks WHERE id = ?", (webhook_id,)
                )
                webhook = cursor.fetchone()
                if not webhook:
                    return jsonify({"error": "Webhook não encontrado"}), 404

                url = webhook[0]
                headers = json.loads(webhook[1]) if webhook[1] else {}

                # Create test payload
                test_payload = {
                    "event": event_type,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "test": True,
                    "data": {
                        "message_id": "TEST-" + str(os.urandom(4).hex()),
                        "phone_number": "+5511999999999",
                        "message": "Esta é uma mensagem de teste do SMS Gateway Web Client",
                        "status": (
                            event_type.split(".")[1] if "." in event_type else "sent"
                        ),
                    },
                }

                import requests

                response = requests.post(
                    url, json=test_payload, headers=headers, timeout=10
                )

                return jsonify(
                    {
                        "success": True,
                        "status_code": response.status_code,
                        "response": response.text[
                            :500
                        ],  # Limit response text to avoid huge data
                    }
                )
            except requests.exceptions.RequestException as e:
                return jsonify(
                    {
                        "success": False,
                        "error": str(e),
                        "status_code": getattr(e.response, "status_code", None),
                        "response": getattr(e.response, "text", "")[:500],
                    }
                )
            except Exception as e:
                return jsonify({"success": False, "error": str(e)})
            finally:
                conn.close()

    cursor.execute("SELECT name, url, events, enabled FROM webhooks ORDER BY name")
    webhooks_data = cursor.fetchall()
    conn.close()

    return render_template("webhooks.html", webhooks=webhooks_data)


# API endpoint to get messages
@app.route("/api/messages", methods=["GET"])
@login_required
def api_messages():
    page = int(request.args.get("page", 1))
    per_page = config.get("messages_per_page", 25)
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    total_pages = (total_messages + per_page - 1) // per_page

    cursor.execute(
        "SELECT id, message, recipients, state, created_at FROM messages ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (per_page, offset),
    )
    messages_data = cursor.fetchall()

    start_index = offset + 1
    end_index = min(offset + per_page, total_messages)

    conn.close()

    return jsonify(
        {
            "messages": messages_data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "start_index": start_index,
                "end_index": end_index,
                "total_messages": total_messages,
            },
        }
    )


# API endpoint to get message details
@app.route("/api/message/<message_id>", methods=["GET"])
@login_required
def api_message_details(message_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, message, recipients, state, created_at FROM messages WHERE id = ?",
        (message_id,),
    )
    message = cursor.fetchone()

    if not message:
        conn.close()
        return jsonify({"error": "Mensagem não encontrada"}), 404

    # Parse recipients
    try:
        recipients = json.loads(message[2])
    except Exception:
        recipients = []

    # For simplicity, mock recipient status since we don't have real per-recipient status in DB
    recipient_data = []
    for phone in recipients:
        recipient_data.append(
            {
                "phoneNumber": phone,
                "state": message[3],  # Use overall message state
                "error": "" if message[3] != "Failed" else "Falha na entrega",
            }
        )

    conn.close()

    return jsonify(
        {
            "id": message[0],
            "message": message[1],
            "state": message[3],
            "createdAt": message[4],
            "recipients": recipient_data,
            "withDeliveryReport": True,  # Mocked for demo
        }
    )


# API endpoint to send SMS
@app.route("/api/send", methods=["POST"])
@login_required
def api_send():
    data = request.get_json()
    message = data.get("message")
    phone_numbers = data.get("phone_numbers", [])
    with_delivery_report = data.get("with_delivery_report", False)
    sim_number = data.get("sim_number")
    ttl = data.get("ttl")

    # Format phone numbers with default country code if needed
    formatted_numbers = []
    country_code = config.get("default_country_code", "+55")
    for number in phone_numbers:
        number = number.strip()
        if number and not number.startswith("+"):
            if not number.startswith(country_code):
                number = country_code + number.lstrip("0")
            formatted_numbers.append(number)
        elif number:
            formatted_numbers.append(number)

    if not formatted_numbers:
        return jsonify({"error": "Nenhum número de telefone fornecido"}), 400

    try:
        client = get_sms_client()
        options = {"with_delivery_report": with_delivery_report}
        if sim_number:
            options["sim_number"] = int(sim_number)
        if ttl:
            options["ttl"] = int(ttl)

        response = client.send_sms(formatted_numbers, message, **options)

        # Store message in database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO messages (id, message, recipients, state, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                response.id,
                message,
                json.dumps(formatted_numbers),
                response.state,
                now,
                now,
            ),
        )
        conn.commit()
        conn.close()

        return jsonify(
            {
                "id": response.id,
                "state": response.state,
                "recipients": formatted_numbers,
            }
        )
    except Exception as e:
        logging.error(f"Error sending SMS: {e}")
        return jsonify({"error": str(e)}), 500


# API endpoint to test connection
@app.route("/api/test-connection", methods=["POST"])
@login_required
def api_test_connection():
    data = request.get_json()
    gateway_url = data.get("gateway_url", config["gateway_url"])
    # api_key = data.get("api_key", config["api_key"]) # Removido pois não é usado
    verify_ssl = data.get("verify_ssl", config["verify_ssl"])

    try:
        # client = AndroidSmsGatewayClient(  # Instanciação do cliente removida, pois não era usada
        #     base_url=gateway_url,
        #     api_key=api_key if api_key else None,
        #     device_id=config["device_id"],
        #     verify_ssl=verify_ssl,
        # )
        # Simple ping or status check - assuming the client has a method to test connection
        # For now, we'll simulate it since the actual client might not have this
        # import requests # Removido daqui, já que foi movido para o topo

        response = requests.get(gateway_url, timeout=5, verify=verify_ssl)
        if response.status_code == 200:
            return jsonify({"success": True})
        else:
            return jsonify(
                {
                    "success": False,
                    "error": f"Resposta inesperada: {response.status_code}",
                }
            )
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Falha na conexão: {str(e)}"})
    except Exception as e:  # Corrigido para Exception as e
        return jsonify({"success": False, "error": f"Erro inesperado: {str(e)}"})
