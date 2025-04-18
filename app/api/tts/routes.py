from flask import Blueprint, request, jsonify, current_app  # Thêm current_app
from gtts import gTTS
from flasgger import swag_from
import io
import cloudinary.uploader
from app.api.tts.models import Vocabulary
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.utils.security import secure_api

tts_bp = Blueprint('tts', __name__)

def process_word_sync(entry, lang, app):
    with app.app_context():
        word = entry.get('word')
        if not word:
            return None

        existing_word = Vocabulary.query.filter_by(word=word).first()
        if existing_word and existing_word.audio:
            print(f"Retrieved existing word: {word}")
            return existing_word.to_dict()

        try:
            print(f"Processing word: {word} with lang: {lang}")
            tts = gTTS(text=word, lang=lang)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            upload_result = cloudinary.uploader.upload(
                audio_buffer,
                resource_type="video",
                format="mp3",
                folder="tts_audio"
            )
            audio_url = upload_result['secure_url']

            entry['audio'] = audio_url
            print(f"Updated '{word}' with audio: {audio_url}")
            return entry

        except Exception as e:
            print(f"Error processing word '{word}': {str(e)}")
            return None

async def process_word(entry, lang, executor, app):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, process_word_sync, entry, lang, app)

@tts_bp.route('/tts', methods=['POST'])
@secure_api(require_signature=True)
@swag_from({
    'tags': ['Text-to-Speech'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'collection': {'type': 'string', 'description': 'The name of the word collection'},
                    'words': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'word': {'type': 'string'},
                                'meaning': {'type': 'string'},
                                'definition': {'type': 'string'},
                                'pronunciation': {'type': 'string'},
                                'partOfSpeech': {'type': 'string'},
                                'audio': {'type': 'string'},
                                'exampleSentence': {'type': 'string'}
                            },
                            'required': ['word']
                        }
                    },
                    'lang': {'type': 'string', 'default': 'en', 'description': 'Language code (e.g., "en", "vi")'},
                    'signature': {'type': 'string', 'description': 'HMAC signature for validation', 'required': True}
                },
                'required': ['words', 'signature']
            }
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication (Enter your API key here)'
        }
    ],
    'responses': {
        '200': {
            'description': 'Updated word list with new audio URLs or existing words',
            'schema': {
                'type': 'object',
                'properties': {
                    'collection': {'type': 'string'},
                    'words': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'word': {'type': 'string'},
                                'meaning': {'type': 'string'},
                                'definition': {'type': 'string'},
                                'pronunciation': {'type': 'string'},
                                'partOfSpeech': {'type': 'string'},
                                'audio': {'type': 'string'},
                                'exampleSentence': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid input format or no valid words provided',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        '401': {
            'description': 'Unauthorized: Invalid or missing API Key',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def text_to_speech_post():
    """Convert a list of dictionary-style words to speech and update their audio URLs."""
    data = request.get_json()
    if not data or 'words' not in data or not isinstance(data['words'], list):
        print("Invalid input:", data)
        return jsonify({"error": "Missing or invalid 'words' parameter (must be a list)"}), 400

    words = data['words']
    lang = data.get('lang', 'en')
    collection = data.get('collection', '')

    if not words:
        print("Words list is empty")
        return jsonify({"error": "Words list cannot be empty"}), 400

    has_valid_word = False
    for entry in words:
        if entry.get('word'):
            has_valid_word = True
            break

    if not has_valid_word:
        print("No valid words in list:", words)
        return jsonify({"error": "No valid words provided (each entry must have a non-empty 'word' field)"}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with ThreadPoolExecutor() as executor:
            app = current_app._get_current_object() 
            tasks = [process_word(entry, lang, executor, app) for entry in words]
            results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

        updated_words = [result for result in results if result is not None and not isinstance(result, Exception)]
        print("Processing results:", results)

        if not updated_words:
            print("No words processed successfully")
            return jsonify({"error": "No valid words processed"}), 400

        return jsonify({
            "collection": collection,
            "words": updated_words
        }), 200

    except Exception as e:
        print("Processing error:", str(e))
        return jsonify({"error": f"Processing failed: {str(e)}"}), 400

    finally:
        loop.close()