import sys
sys.path.append("../")
sys.path.append("../app")

from fastapi import Response, APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import app


########### Test model and router ###########
class test_model_in(BaseModel):
    test_name: str
    test_number: int

class test_model_out(BaseModel):
    test_number: int

router = APIRouter()

@router.get("/logging/param", response_model = test_model_out)
async def param_test(name: str = None, number: int = None) -> Response:
    return test_model_out(test_number = number)


@router.post("/logging/json", response_model = test_model_out)
async def model_test(test_model: test_model_in) -> Response:
    return test_model


#############################################

########### Test client ###########
app.include_router(router = router, tags = ["test"], prefix = "/api/test")

client = TestClient(app)

def test_param_logging():
    test_name = "teeeessssttttt"
    test_number = 0

    response = client.get(f"/api/test/logging/param?name={test_name}&number={test_number}")

    assert response.status_code == 200
    assert response.json() == {
        "test_name": test_name,
        "test_number": test_number
    }


def test_model_logging():
    test_name = "test"
    test_number = 1

    response = client.post("/api/test/logging/json", json = {"test_name": test_name, "test_number": test_number})

    assert response.status_code == 200
    assert response.json() == {
        "test_name": test_name,
        "test_number": test_number
    }


if __name__ == "__main__":
    test_param_logging()
    test_model_logging()