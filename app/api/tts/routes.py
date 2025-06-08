from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.utils.security import secure_api
from app.services.tts_service import process_word_sync

tts_bp = Blueprint('tts', __name__)

async def process_word(entry, lang, executor, app):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, process_word_sync, entry, lang, app)

@tts_bp.route('/tts', methods=['POST'])
@secure_api(require_signature=True)
def text_to_speech_post():
    data = request.get_json()
    if not data or not isinstance(data.get('words'), list):
        return jsonify({"error": "Missing or invalid 'words' parameter"}), 400

    words = data['words']
    lang = data.get('lang', 'en')
    collection = data.get('collection', '')

    if not any(entry.get('word') for entry in words):
        return jsonify({"error": "No valid words provided"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        app = current_app._get_current_object()
        with ThreadPoolExecutor() as executor:
            tasks = [process_word(entry, lang, executor, app) for entry in words]
            results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

        updated_words = [res for res in results if isinstance(res, dict)]

        if not updated_words:
            return jsonify({"error": "No valid words processed"}), 400

        return jsonify({
            "collection": collection,
            "words": updated_words
        }), 200

    except Exception as e:
        current_app.logger.error(f"[Fatal] Processing failed: {str(e)}", exc_info=True)
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

    finally:
        loop.close()
