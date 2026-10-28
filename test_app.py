
import os
import tempfile
import importlib

def test_health_endpoint():
    with tempfile.TemporaryDirectory() as folder:
        os.environ["DATA_DIR"] = folder
        os.environ["APP_VERSION"] = "v1"
        import app
        importlib.reload(app)
        response = app.app.test_client().get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"
        importlib.reload(app)
