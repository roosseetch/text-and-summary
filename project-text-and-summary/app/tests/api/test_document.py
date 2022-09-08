import factory

from app.models.document import Document
from app.tests.factories import DocumentFactory


def test_retrieve_summary(client):
    """
    test retriving of summary
    """
    doc = DocumentFactory.create()
    response = client.get(f'/summaries/{doc.id}')
    res = response.json()
    assert response.status_code == 200
    assert set(res.keys()) == set(['id', 'summary'])
    assert doc.id == res['id']


def test_retrieve_document(client):
    """
    test retriving of document
    """
    doc = DocumentFactory.create()
    response = client.get(f'/{doc.id}')
    res = response.json()
    assert response.status_code == 200
    assert set(res.keys()) == set(['id', 'text', 'summary'])
    assert doc.id == res['id']


def test_list_documents(client):
    """
    test listing of documents
    """
    DocumentFactory.create_batch(3)
    response = client.get('/')
    res = response.json()
    assert response.status_code == 200
    assert len(res['results']) == 3
    assert list(res['results'][0].keys()) == ['id']


def test_create_document(client):
    """
    test creation of documents
    """
    data = {
        'text': factory.Faker('text')
    }
    response = client.post('/', data=data)
    res = response.json()
    assert response.status_code == 201
    assert list(res.keys()) == ['id']
    assert res['id'] == 1


def test_update_document(client, session):
    """
    test updating of documents
    """
    doc = DocumentFactory.create()
    initial_text = doc.text
    faker = factory.faker.faker.Faker()
    data = {
        'text': faker.text()
    }
    response = client.put(f'/{doc.id}', data=data)
    res = response.json()
    assert response.status_code == 200
    assert list(res.keys()) == ['id']
    assert res['id'] == 1

    updated_doc = list(session())[0].query(Document).one()

    assert initial_text != data['text']
    assert updated_doc.text == data['text']
    # because of db.refresh(db_obj) in CRUD creat method we have valid next assertion
    assert updated_doc.text == doc.text
