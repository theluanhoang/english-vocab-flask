from gtts import gTTS
import io
import cloudinary.uploader
from app.api.tts.models import Vocabulary
from flask import current_app

def generate_audio(word: str, lang: str) -> io.BytesIO:
    tts = gTTS(text=word, lang=lang)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer

def upload_audio_to_cloudinary(buffer: io.BytesIO) -> str:
    upload_result = cloudinary.uploader.upload(
        buffer,
        resource_type="video",
        format="mp3",
        folder="tts_audio"
    )
    return upload_result['secure_url']

def process_word_sync(entry, lang, app):
    with app.app_context():
        word = entry.get('word')
        if not word:
            return None

        existing_word = Vocabulary.query.filter_by(word=word).first()
        if existing_word and existing_word.audio:
            current_app.logger.info(f"[Cached] Retrieved existing word: {word}")
            return existing_word.to_dict()

        try:
            audio_buffer = generate_audio(word, lang)
            audio_url = upload_audio_to_cloudinary(audio_buffer)
            entry['audio'] = audio_url
            current_app.logger.info(f"[Upload] Word '{word}' audio uploaded: {audio_url}")
            return entry
        except Exception as e:
            current_app.logger.error(f"[Error] Word '{word}': {str(e)}", exc_info=True)
            return None