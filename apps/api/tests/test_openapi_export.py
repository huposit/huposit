import json

from app.tools.export_openapi import export_openapi


def test_export_openapi_writes_health_schema(tmp_path):
    output_path = tmp_path / "openapi.json"

    export_openapi(output_path)

    schema = json.loads(output_path.read_text(encoding="utf-8"))

    assert schema["paths"]["/health"]["get"]["operationId"] == "getServerHealth"
    assert schema["paths"]["/health/db"]["get"]["operationId"] == "getDatabaseHealth"
    assert schema["paths"]["/health/worker"]["get"]["operationId"] == "getWorkerHealth"
    assert "HealthResponse" in schema["components"]["schemas"]
    assert "DatabaseHealthResponse" in schema["components"]["schemas"]
    assert "WorkerHealthResponse" in schema["components"]["schemas"]
