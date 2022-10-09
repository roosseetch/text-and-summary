import factory

from unittest.mock import patch, Mock

from app.models.document import Document
from app.tests.factories import DocumentFactory
from app.utils.string_utils import strip_special_characters


def test_cors_middlewares_valid_origin(client):
    """
    test CORS middleware with valid Origin
    """
    headers = {
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'origin',
        'Origin': 'http://localhost:8001'
    }
    response = client.options('/', headers=headers)
    assert response.status_code == 200
    assert response.text == 'OK'
    assert response.headers['access-control-allow-origin'] == 'http://localhost:8001'


def test_cors_middlewares_not_valid_origin(client):
    """
    test CORS middleware with NOT valid Origin
    """
    headers = {
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'origin',
        'Origin': 'http://fake-url.fake'
    }
    response = client.options('/', headers=headers)
    assert response.status_code == 400
    assert response.text == 'Disallowed CORS origin'
    assert 'access-control-allow-origin' not in response.headers


def test_process_time_middleware(client):
    """
    test ProcessTimeMiddleware
    """
    response = client.get('/')
    res = response.json()
    assert response.status_code == 200
    assert len(res['results']) == 0
    assert 'x-process-time' in response.headers


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


def test_list_documents_with_skip(client):
    """
    test listing of documents
    """
    DocumentFactory.create_batch(3)
 
    params = {'skip': 2}
    response = client.get('/', params=params)
    res = response.json()
    assert response.status_code == 200
    assert len(res['results']) == 1
 
    params = {'skip': -1}
    response = client.get('/', params=params)
    assert response.status_code == 422
 
    '''
    Test that in SQL `OFFSET %(param_2)` less then 9223372036854775807 BIGINT
    to avoid the error `sqlalchemy.exc.DataError: (psycopg2.errors.NumericValueOutOfRange)
    bigint out of range`
    '''
    params = {'skip': 99999999999999999999999999999999999999999999999999}
    response = client.get('/', params=params)
    assert response.status_code == 422


def test_list_documents_with_limit(client):
    """
    test listing of documents with `limit` query parameter
    """
    DocumentFactory.create_batch(3)
 
    params = {'limit': 1}
    response = client.get('/', params=params)
    res = response.json()
    assert response.status_code == 200
    assert len(res['results']) == 1
 
    params = {'limit': -1}
    response = client.get('/', params=params)
    assert response.status_code == 422
 
    '''
    Test that in SQL `OFFSET %(param_2)` less then 9223372036854775807 BIGINT
    to avoid the error `sqlalchemy.exc.DataError: (psycopg2.errors.NumericValueOutOfRange)
    bigint out of range`
    '''
    params = {'limit': 99999999999999999999999999999999999999999999999999}
    response = client.get('/', params=params)
    assert response.status_code == 422


@patch('app.tasks.document_tasks.generate_summary_for_text', Mock())
def test_create_document(client, session):
    """
    test creation of documents
    """
    text = factory.faker.faker.Faker().text().strip('.')
    data = {
        'text': ''.join([text, '.&(&((%&$%^$^'])
    }
    response = client.post('/', data=data)
    res = response.json()
    assert response.status_code == 201
    assert list(res.keys()) == ['id']
    assert res['id'] == 1

    doc = list(session())[0].query(Document).one()
    assert text == doc.text


@patch('app.tasks.document_tasks.generate_summary_for_text', Mock())
def test_update_document(client, session):
    """
    test updating of documents
    """
    doc = DocumentFactory.create()
    initial_text = doc.text
    text = factory.faker.faker.Faker().text().strip('.')
    data = {
        'text': ''.join([text, '.&(&((%&$%^$^'])
    }
    response = client.put(f'/{doc.id}', data=data)
    res = response.json()
    assert response.status_code == 200
    assert list(res.keys()) == ['id']
    assert res['id'] == 1

    updated_doc = list(session())[0].query(Document).one()

    assert initial_text != data['text']
    assert updated_doc.text == strip_special_characters(data['text'])
    # because of db.refresh(db_obj) in CRUD creat method we have valid next assertion
    assert updated_doc.text == doc.text


@patch('app.tasks.document_tasks.generate_summary_for_text', Mock())
def test_create_document_with_empty_text(client):
    """
    test creation of documents
    """
    data = {
        'text': ''
    }
    response = client.post('/', data=data)
    res = response.json()
    assert response.status_code == 422
    assert res['message'][0] == 'text: none is not an allowed value'


@patch('app.tasks.document_tasks.generate_summary_for_text', Mock())
def test_create_document_with_text_just_special_characters(client):
    """
    test creation of documents
    """
    data = {
        'text': '&*^@(#&@(*#@!##@_)#@#&@#)(@#@#$%^&_)^%@!'
    }
    response = client.post('/', data=data)
    res = response.json()
    assert response.status_code == 422
    assert res['message'][0] == 'text: Text should contain not special characters'
