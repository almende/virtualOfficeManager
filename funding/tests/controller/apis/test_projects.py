import copy

api_version = "v1"
base_url = '/api/{}/projects/'.format(api_version)

example_project = {"title": "x", "description": "dx"}
obj_name = "project"


def remove_ids(json):
    json = copy.deepcopy(json)
    for o in json:
        del o["_id"]

    return json


def test_get_all_projects_redirect(client):
    response = client.get(base_url[:-1])

    assert response.status_code == 308
    assert response.get_json() is None
    assert response.location.endswith(base_url)


def test_get_all_projects_empty(client):
    response = client.get(base_url)

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_projects(client):
    data = [example_project,
            {"title": "y", "description": "dy"}]
    client.post(base_url, json=data[0])
    client.post(base_url, json=data[1])
    response = client.get(base_url)

    assert remove_ids(response.get_json()) == data
    assert response.status_code == 200


def test_post_project_ok(client):
    response = client.post(base_url, json=example_project)

    assert response.get_json() == remove_ids([response.get_json()])[0]
    assert response.status_code == 201


# TODO
# def test_post_project_not_ok(client, db):
#     response = client.post(base_url, json="...")
#
#     assert response.status_code == 400
#     assert response.get_json() == {"message": '...'}


def test_delete_existing_project(client, db):
    post_response = client.post(base_url, json=example_project)

    response = client.delete(base_url + post_response.json["_id"])

    assert response.status_code == 204


def test_delete_nonexisting_project_bad_id(client):
    uid = 'non_existing_project_resulting_in_exception'
    response = client.delete(base_url + uid)

    assert response.status_code == 404
    assert response.get_json() == {"message": "{} {} not found".format(obj_name, uid)}


def test_delete_nonexisting_project_ok_id(client):
    uid = '0123456789ab0123456789ab' # must be 12-byte input or 24-character hex string to be converted to ObjectID
    response = client.delete(base_url + uid)

    assert response.status_code == 404
    assert response.get_json() == {"message": "{} {} not found".format(obj_name, uid)}


def test_patch_existing_project(client):  # TODO: Test whenever name is not changed.
    post_response = client.post(base_url, json=example_project)
    overwritejson = copy.deepcopy(post_response.json)
    overwritejson["title"] = "something else"


    response = client.patch(base_url + post_response.json["_id"], json={"title": overwritejson["title"]})

    assert response.status_code == 200
    assert response.json == overwritejson
