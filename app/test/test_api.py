from collections import Counter
from fastapi.testclient import TestClient
from main import app


def test_api():
    with TestClient(app) as client:
        # Test read_root
        response = client.get('/')
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert 'active models' in response_json
        active_models = response_json.get('active models').keys()

        # Test models_list
        response = client.get('/models_list')
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert 'models' in response_json

        # Test predict_label with all codifications
        response = client.get('/label?q=orange&v=True')
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert Counter(response_json.keys()) == Counter(active_models)
        value = next(iter(response_json))
        assert 'orange' in response_json.get(value)
        assert isinstance(response_json.get(value).get('orange'), list)
        assert len(response_json.get(value).get('orange')) == 1
        for key in ('label', 'proba', 'confiance'):
            assert key in response_json.get(value).get('orange')[0]
        assert '|' in response_json.get(value).get('orange')[0].get('label')
        assert float(response_json.get(value).get('orange')[0].get('proba')) <= 1
        assert float(response_json.get(value).get('orange')[0].get('confiance')) <= 1

        # Test predict_label with only one classification
        response = client.get('/label?q=orange&n=na2008')
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert list(response_json.keys()) == ['na2008']

        # Test predict_label with multiple descriptions
        response = client.get('/label?q=orange&q=pain&n=na2008')
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert Counter(response_json.get('na2008').keys()) == Counter(['pain', 'orange'])

        # Test predict_label with k > 1
        response = client.get('/label?q=orange&n=na2008&k=2')
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert isinstance(response_json.get('na2008').get('orange'), list)
        assert len(response_json.get('na2008').get('orange')) == 2

        # Test process
        response = client.get("/process?q=jus d'orange")
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert list(response_json.keys()) == ["jus d'orange"]
        assert response_json.get("jus d'orange") == "JUS ORANGE"

        # Test process with list of descriptions
        response = client.get("/process?q=jus d'orange&q=pot de^ nutella")
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert Counter(response_json.keys()) == Counter(["jus d'orange", "pot de^ nutella"])
        assert response_json.get("jus d'orange") == "JUS ORANGE"
        assert response_json.get("pot de^ nutella") == "POT DE NUTELLA"

        # Test label_description
        response = client.get("/label_description?q=J61Z")
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert response_json.get('J61Z') == 'Télécommunications'

        # Test label_description with list of labels
        response = client.get("/label_description?q=J61Z&q=01.1.8.2.1")
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert response_json.get('J61Z') == 'Télécommunications'
        assert response_json.get('01.1.8.2.1') == 'Confitures, compotes et miel'
