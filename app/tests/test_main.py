import os
from shutil import copy2

from fastapi.testclient import TestClient

for file in ["test_shelve.db.dat", "test_shelve.db.dir", "test_shelve.db.bak"]:
    copy2(f"app/tests/{file}", "/tmp")

os.environ["SHELVE_PATH"] = "/tmp/test_shelve.db"
from app.main import app  # noqa: E402

client = TestClient(app)

task_1 = {
    "title": "Some title",
    "description": "Some description",
    "task_id": 1,
    "date": "2021-01-12T09:03:30.980303",
    "status": "Pending",
}
task_2 = {
    "title": "Another title",
    "description": "Another descrition",
    "task_id": 2,
    "date": "2021-01-12T09:04:30.980303",
    "status": "Pending",
}
task_3 = {
    "title": "And now...",
    "description": "something complitly diferent",
    "task_id": 3,
    "date": "2021-01-12T09:05:30.980303",
    "status": "Pending",
}

task_post = {
    "title": "nobody expect the spanish inquisition",
    "description": "our weapons are fear and surpice!",
}


def test_get_all():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {"message": "ok", "result": [task_1, task_2, task_3]}


def test_get_one():
    response = client.get("/task/1")
    assert response.status_code == 200
    assert response.json() == {"message": "ok", "result": task_1}


def test_get_one_invalid():
    response = client.get("/task/999")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid task_id: 'task_id 999' don't exist."}


def test_post():
    response = client.post("/task", json=task_post)
    assert response.status_code == 200
    result = response.json()["result"]
    assert result["title"] == task_post["title"]
    assert result["description"] == task_post["description"]
    assert result["task_id"] == 4
    assert result["status"] == "Pending"


def test_post_missing_title():
    response = client.post("/task", json={"description": task_post["description"]})
    assert response.status_code == 422


def test_post_missing_description():
    response = client.post("/task", json={"title": task_post["title"]})
    assert response.status_code == 422


def test_put():
    response = client.put("/task/1", params={"status": "done"})
    assert response.status_code == 200
    assert response.json() == {"message": "ok", "result": {**task_1, "status": "Done"}}


def test_put_invalid_param():
    response = client.put("/task/1", params={"status": "spam"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Query parameter 'status' invalid. Should be 'Done', 'Pending' or 'Cancel'"
    }


def test_put_invalid_task_id():
    response = client.put("/task/999", params={"status": "done"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid task_id: 'task_id 999' don't exist."}


def test_delete():
    response = client.delete("/task/1")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_delete_invalid_task_id():
    response = client.delete("/task/999")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid task_id: 'task_id 999' don't exist."}
