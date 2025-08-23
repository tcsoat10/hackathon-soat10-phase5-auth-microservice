from fastapi import status

def test_health_check_v1(client):
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
