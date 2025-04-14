from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument
from datetime import datetime

class Experience(EmbeddedDocument):
    title = StringField(max_length=200)
    duration = StringField(max_length=200)
    responsibilities = StringField(max_length=5000)

class ParsedResume(Document):
    user_id = StringField(required=True)
    text = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'parsed_resumes',
        'indexes': [
            'user_id'
        ],
        'db_alias': 'default',
    }