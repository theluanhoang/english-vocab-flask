# from flask import Blueprint, request, jsonify
# from gtts import gTTS
# from flasgger import swag_from
# import io
# import cloudinary.uploader

# tts_bp = Blueprint('tts', __name__)

# @tts_bp.route('/tts', methods=['POST'])
# @swag_from({
#     'tags': ['Text-to-Speech'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'collection': {
#                         'type': 'string',
#                         'description': 'The name of the word collection'
#                     },
#                     'words': {
#                         'type': 'array',
#                         'items': {
#                             'type': 'object',
#                             'properties': {
#                                 'word': {'type': 'string'},
#                                 'meaning': {'type': 'string'},
#                                 'definition': {'type': 'string'},
#                                 'pronunciation': {'type': 'string'},
#                                 'partOfSpeech': {'type': 'string'},
#                                 'audio': {'type': 'string'},
#                                 'exampleSentence': {'type': 'string'}
#                             },
#                             'required': ['word']
#                         }
#                     },
#                     'lang': {
#                         'type': 'string',
#                         'default': 'en',
#                         'description': 'Language code (e.g., "en", "vi")'
#                     }
#                 },
#                 'required': ['words']
#             }
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Updated word list with new audio URLs',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'collection': {'type': 'string'},
#                     'words': {
#                         'type': 'array',
#                         'items': {'type': 'object'}
#                     }
#                 }
#             }
#         },
#         '400': {
#             'description': 'Invalid input format'
#         }
#     }
# })
# def text_to_speech_post():
#     """Convert a list of dictionary-style words to speech and update their audio URLs."""
#     data = request.get_json()
#     if not data or 'words' not in data or not isinstance(data['words'], list):
#         return {"error": "Missing or invalid 'words' parameter (must be a list)"}, 400

#     words = data['words']
#     lang = data.get('lang', 'en')
#     collection = data.get('collection', '')

#     if not words:
#         return {"error": "Words list cannot be empty"}, 400

#     updated_words = []

#     try:
#         for entry in words:
#             word = entry.get('word')
#             if not word:
#                 continue

#             print(f"Processing word: {word} with lang: {lang}")
            
#             tts = gTTS(text=word, lang=lang)
#             audio_buffer = io.BytesIO()
#             tts.write_to_fp(audio_buffer)
#             audio_buffer.seek(0)

#             upload_result = cloudinary.uploader.upload(
#                 audio_buffer,
#                 resource_type="video",
#                 format="mp3"
#             )
#             audio_url = upload_result['secure_url']

#             entry['audio'] = audio_url
#             updated_words.append(entry)

#             print(f"Updated '{word}' with audio: {audio_url}")

#         return jsonify({
#             "collection": collection,
#             "words": updated_words
#         }), 200

#     except Exception as e:
#         return {"error": str(e)}, 400


# from flask import Blueprint, request, jsonify
# from gtts import gTTS
# from flasgger import swag_from
# import io, os
# import cloudinary.uploader

# tts_bp = Blueprint('tts', __name__)

# # API Key bí mật (lấy từ biến môi trường để bảo mật)
# API_KEY = os.getenv('API_KEY')  # Đảm bảo biến môi trường API_KEY được thiết lập

# def verify_api_key():
#     api_key = request.headers.get('X-API-Key')
#     if not api_key or api_key != API_KEY:
#         return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401
#     return None

# @tts_bp.route('/tts', methods=['POST'])
# @swag_from({
#     'tags': ['Text-to-Speech'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'collection': {
#                         'type': 'string',
#                         'description': 'The name of the word collection'
#                     },
#                     'words': {
#                         'type': 'array',
#                         'items': {
#                             'type': 'object',
#                             'properties': {
#                                 'word': {'type': 'string'},
#                                 'meaning': {'type': 'string'},
#                                 'definition': {'type': 'string'},
#                                 'pronunciation': {'type': 'string'},
#                                 'partOfSpeech': {'type': 'string'},
#                                 'audio': {'type': 'string'},
#                                 'exampleSentence': {'type': 'string'}
#                             },
#                             'required': ['word']
#                         }
#                     },
#                     'lang': {
#                         'type': 'string',
#                         'default': 'en',
#                         'description': 'Language code (e.g., "en", "vi")'
#                     }
#                 },
#                 'required': ['words'],
#                 'example': {
#                     'collection': 'sample_collection',
#                     'words': [
#                         {'word': 'hello', 'meaning': 'xin chào', 'partOfSpeech': 'noun'},
#                         {'word': 'world', 'meaning': 'thế giới', 'partOfSpeech': 'noun'}
#                     ],
#                     'lang': 'en'
#                 }
#             }
#         },
#         {
#             'name': 'X-API-Key',
#             'in': 'header',
#             'type': 'string',
#             'required': True,
#             'description': 'API Key for authentication (Enter your API key here)',
#             'default': ''  # Để trống, yêu cầu người dùng nhập thủ công trong Swagger UI
#         }
#     ],
#     'responses': {
#         '200': {
#             'description': 'Updated word list with new audio URLs',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'collection': {'type': 'string'},
#                     'words': {
#                         'type': 'array',
#                         'items': {
#                             'type': 'object',
#                             'properties': {
#                                 'word': {'type': 'string'},
#                                 'meaning': {'type': 'string'},
#                                 'definition': {'type': 'string'},
#                                 'pronunciation': {'type': 'string'},
#                                 'partOfSpeech': {'type': 'string'},
#                                 'audio': {'type': 'string'},
#                                 'exampleSentence': {'type': 'string'}
#                             }
#                         }
#                     }
#                 },
#                 'example': {
#                     'collection': 'sample_collection',
#                     'words': [
#                         {'word': 'hello', 'meaning': 'xin chào', 'partOfSpeech': 'noun', 'audio': 'https://res.cloudinary.com/your_cloud/video/upload/v1234567890/hello.mp3'},
#                         {'word': 'world', 'meaning': 'thế giới', 'partOfSpeech': 'noun', 'audio': 'https://res.cloudinary.com/your_cloud/video/upload/v1234567890/world.mp3'}
#                     ]
#                 }
#             }
#         },
#         '400': {
#             'description': 'Invalid input format',
#             'schema': {
#                 'type': 'object',
#                 'properties': {'error': {'type': 'string'}}
#             }
#         },
#         '401': {
#             'description': 'Unauthorized: Invalid or missing API Key',
#             'schema': {
#                 'type': 'object',
#                 'properties': {'error': {'type': 'string'}}
#             }
#         }
#     }
# })
# def text_to_speech_post():
#     """Convert a list of dictionary-style words to speech and update their audio URLs."""
#     auth_error = verify_api_key()
#     if auth_error:
#         return auth_error

#     data = request.get_json()
#     if not data or 'words' not in data or not isinstance(data['words'], list):
#         return {"error": "Missing or invalid 'words' parameter (must be a list)"}, 400

#     words = data['words']
#     lang = data.get('lang', 'en')
#     collection = data.get('collection', '')

#     if not words:
#         return {"error": "Words list cannot be empty"}, 400

#     updated_words = []

#     try:
#         for entry in words:
#             word = entry.get('word')
#             if not word:
#                 continue

#             print(f"Processing word: {word} with lang: {lang}")
#             tts = gTTS(text=word, lang=lang)
#             audio_buffer = io.BytesIO()
#             tts.write_to_fp(audio_buffer)
#             audio_buffer.seek(0)

#             upload_result = cloudinary.uploader.upload(
#                 audio_buffer,
#                 resource_type="video",
#                 format="mp3"
#             )
#             audio_url = upload_result['secure_url']

#             entry['audio'] = audio_url
#             updated_words.append(entry)

#             print(f"Updated '{word}' with audio: {audio_url}")

#         return jsonify({
#             "collection": collection,
#             "words": updated_words
#         }), 200

#     except Exception as e:
#         return {"error": str(e)}, 400

from flask import Blueprint, request, jsonify
from gtts import gTTS
from flasgger import swag_from
import io, os
import cloudinary.uploader

tts_bp = Blueprint('tts', __name__)

API_KEY = os.getenv('API_KEY')

def verify_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != API_KEY:
        return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401
    return None

@tts_bp.route('/tts', methods=['POST'])
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
                    'lang': {'type': 'string', 'default': 'en', 'description': 'Language code (e.g., "en", "vi")'}
                },
                'required': ['words']
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
        '200': {'description': 'Updated word list with new audio URLs', 'schema': {...}},
        '400': {'description': 'Invalid input format or no valid words provided'},
        '401': {'description': 'Unauthorized: Invalid or missing API Key'}
    }
})
def text_to_speech_post():
    """Convert a list of dictionary-style words to speech and update their audio URLs."""
    auth_error = verify_api_key()
    if auth_error:
        return auth_error

    data = request.get_json()
    if not data or 'words' not in data or not isinstance(data['words'], list):
        return jsonify({"error": "Missing or invalid 'words' parameter (must be a list)"}), 400

    words = data['words']
    lang = data.get('lang', 'en')
    collection = data.get('collection', '')

    if not words:
        return jsonify({"error": "Words list cannot be empty"}), 400

    updated_words = []
    has_valid_word = False

    try:
        for entry in words:
            word = entry.get('word')
            if not word:  # Bỏ qua nếu không có 'word' hoặc 'word' rỗng
                continue
            has_valid_word = True
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
            updated_words.append(entry)

            print(f"Updated '{word}' with audio: {audio_url}")

        if not has_valid_word:
            return jsonify({"error": "No valid words provided (each entry must have a non-empty 'word' field)"}), 400

        return jsonify({
            "collection": collection,
            "words": updated_words
        }), 200

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 400