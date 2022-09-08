import factory

from app.models.document import Document

class DocumentFactory(factory.alchemy.SQLAlchemyModelFactory):
    text = factory.Faker('text', max_nb_chars=300)
    summary = factory.Faker('text', max_nb_chars=30)
 
    class Meta:
        model = Document
        sqlalchemy_session_persistence = 'commit'
