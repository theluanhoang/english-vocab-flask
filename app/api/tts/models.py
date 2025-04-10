from app.extensions import db
from datetime import datetime

class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    pronunciation = db.Column(db.String(255), nullable=False)
    example_sentence = db.Column(db.Text, nullable=False)
    part_of_speech = db.Column(db.String(50), nullable=False)
    audio = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

    collection_vocabularies = db.relationship('CollectionVocabulary', backref='vocabulary', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'definition': self.definition,
            'pronunciation': self.pronunciation,
            'example_sentence': self.example_sentence,
            'part_of_speech': self.part_of_speech,
            'audio': self.audio,
            'created_at': self.created_at.isoformat()
        }

class CollectionVocabulary(db.Model):
    __tablename__ = 'collection_vocabulary'

    id = db.Column(db.Integer, primary_key=True)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'vocabulary_id': self.vocabulary_id,
            'created_at': self.created_at.isoformat()
        }