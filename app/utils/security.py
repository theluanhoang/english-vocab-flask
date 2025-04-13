# app/utils/security.py
from flask import request, jsonify, current_app
import hmac, hashlib, json

def load_config():
    return {
        "API_KEYS": current_app.config.get("API_KEYS", []),
        "HMAC_SECRET_KEY": current_app.config.get("HMAC_SECRET_KEY", b"default_secret"),
        "ALLOWED_IPS": current_app.config.get("ALLOWED_IPS", ["127.0.0.1"])
    }

def is_valid_hmac_signature(data, signature, secret_key):
    try:
        print(signature)
        print(secret_key)
        payload = json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode()
        expected = hmac.new(secret_key, payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
    except Exception:
        return False

def secure_api(require_signature=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            cfg = load_config()

            # API Key
            api_key = request.headers.get('X-API-Key').strip()
            if not api_key or api_key not in cfg["API_KEYS"]:
                return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401

            # IP Whitelist
            if request.remote_addr not in cfg["ALLOWED_IPS"]:
                return jsonify({"error": f"Forbidden: IP {request.remote_addr} not allowed"}), 403

            # HMAC Signature
            if require_signature:
                json_data = request.get_json()
                if not json_data or 'words' not in json_data:
                    return jsonify({"error": "Invalid or missing JSON data"}), 400

                signature = json_data.get("signature")
                if not signature or not is_valid_hmac_signature(json_data['words'], signature, cfg["HMAC_SECRET_KEY"]):
                    return jsonify({"error": "Invalid or missing HMAC signature"}), 401

            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
