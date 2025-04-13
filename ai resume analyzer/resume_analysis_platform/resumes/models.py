from mongoengine import Document, StringField, ListField, IntField, EmbeddedDocument, EmbeddedDocumentField

class Experience(EmbeddedDocument):
    title = StringField(max_length=100)
    duration = StringField(max_length=50)  # e.g., "2 years"
    responsibilities = StringField()

class ParsedResume(Document):
    user_id = StringField(required=True)  # Reference to User ID (not a ForeignKey since it's MongoDB)
    skills = ListField(StringField(max_length=50))
    experience = ListField(EmbeddedDocumentField(Experience))
    education = StringField()
    certifications = ListField(StringField(max_length=100))
    match_scores = ListField(IntField())  # For storing job match scores
    feedback = StringField()

    meta = {
        'collection': 'parsed_resumes',
        'db_alias': 'default',  # MongoDB connection is handled by mongoengine
    }