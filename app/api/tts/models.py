from app.extensions import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Vocabulary(db.Model):
    __tablename__ = 'vocabularies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word = db.Column(db.String(255), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    pronunciation = db.Column(db.String(255), nullable=False)
    example_sentence = db.Column(db.Text, nullable=False)
    part_of_speech = db.Column(db.String(50), nullable=False)
    audio = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow) 
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow) 

    collection_vocabularies = db.relationship('CollectionVocabulary', backref='vocabulary', lazy=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'word': self.word,
            'definition': self.definition,
            'pronunciation': self.pronunciation,
            'exampleSentence': self.example_sentence,
            'partOfSpeech': self.part_of_speech,
            'audio': self.audio,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'deletedAt': self.deleted_at.isoformat() if self.deleted_at else None,
            'collectionVocabularies': [cv.to_dict() for cv in self.collection_vocabularies]
        }

class CollectionVocabulary(db.Model):
    __tablename__ = 'collection_vocabularies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vocabulary_id = db.Column(UUID(as_uuid=True), db.ForeignKey('vocabularies.id'), nullable=False)
    collection_id = db.Column(UUID(as_uuid=True), db.ForeignKey('collections.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow) 
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow) 

    def to_dict(self):
        return {
            'id': str(self.id),
            'vocabularyId': str(self.vocabulary_id),
            'collectionId': str(self.collection_id),
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'deletedAt': self.deleted_at.isoformat() if self.deleted_at else None,
        }