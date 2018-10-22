def test_cors_header_present_on_get(client_cors):
    """Test that a CORS header is present on GET requests"""
    response = client_cors.get('/v0.1/backend')
    assert response.status_code == 200
    assert response.headers.has_key('Access-Control-Allow-Origin')

def test_cors_header_present_on_options(client_cors):
    """Test that a CORS header is present on OPTIONS requests"""
    response = client_cors.options('/v0.1/backend')
    assert response.status_code == 200
    assert response.headers.has_key('Access-Control-Allow-Origin')

def test_cors_header_no_origin_on_get(client_cors):
    """Test that a CORS header is present on GET requests and equal to a wildcard without an origin header"""
    response = client_cors.get('/v0.1/backend')
    assert response.status_code == 200
    assert response.headers.has_key('Access-Control-Allow-Origin')
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

def test_cors_header_no_origin_on_options(client_cors):
    """Test that a CORS header is present on OPTIONS requests and equal to a wildcard without an origin header"""
    response = client_cors.options('/v0.1/backend')
    assert response.status_code == 200
    assert response.headers.has_key('Access-Control-Allow-Origin')
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

def test_cors_header_with_origin_on_get(client_cors):
    """Test that a CORS header is present on GET requests and equal to right domain when an origin header is specified"""
    response = client_cors.get('/v0.1/backend', headers={'Origin': 'example.invalid'})
    assert response.status_code == 200
    assert response.headers.has_key('Access-Control-Allow-Origin')
    assert response.headers.get('Access-Control-Allow-Origin') == 'example.invalid'

def test_cors_header_with_origin_on_options(client_cors):
    """Test that a CORS header is present on OPTIONS requests and equal to right domain when an origin header is specified"""
    response = client_cors.options('/v0.1/backend', headers={'Origin': 'example.invalid'})
    assert response.status_code == 200
    assert response.headers.has_key('Access-Control-Allow-Origin')
    assert response.headers.get('Access-Control-Allow-Origin') == 'example.invalid'

def test_cors_header_not_present_on_get(client):
    """Test that a CORS header is NOT present with CORS disabled"""
    response = client.get('/v0.1/backend')
    assert response.status_code == 200
    assert not response.headers.has_key('Access-Control-Allow-Origin')

def test_cors_header_not_present_on_options(client):
    """Test that a CORS header is NOT present with CORS disabled"""
    response = client.options('/v0.1/backend')
    assert response.status_code == 200
    assert not response.headers.has_key('Access-Control-Allow-Origin')