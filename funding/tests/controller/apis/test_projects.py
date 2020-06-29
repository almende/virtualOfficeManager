import copy

api_version = "v1"
base_url = '/api/{}/projects/'.format(api_version)

example_project = {"title": "x", "description": "dx"}
obj_name = "project"
api_key_header = {'X-API-KEY': 'fake key'}


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
    client.post(base_url, json=data[0], headers=api_key_header)
    client.post(base_url, json=data[1], headers=api_key_header)
    response = client.get(base_url)

    assert response.status_code == 200
    assert remove_ids(response.get_json()) == data


def test_post_project_ok(client):
    response = client.post(base_url, json=example_project, headers=api_key_header)

    assert remove_ids([response.get_json()])[0] == example_project
    assert response.status_code == 201


# TODO
# def test_post_project_not_ok(client, db):
#     response = client.post(base_url, json="...")
#
#     assert response.status_code == 400
#     assert response.get_json() == {"message": '...'}


def test_delete_existing_project(client):
    post_response = client.post(base_url, json=example_project, headers=api_key_header)

    response = client.delete(base_url + post_response.json["_id"], headers=api_key_header)

    assert response.status_code == 204


def test_delete_nonexisting_project_bad_id(client):
    uid = 'non_existing_project_resulting_in_exception'
    response = client.delete(base_url + uid, headers=api_key_header)

    assert response.status_code == 404
    assert response.get_json() == {"message": "{} {} not found".format(obj_name, uid)}


def test_delete_nonexisting_project_ok_id(client):
    uid = '0123456789ab0123456789ab' # must be 12-byte input or 24-character hex string to be converted to ObjectID
    response = client.delete(base_url + uid, headers=api_key_header)

    assert response.status_code == 404
    assert response.get_json() == {"message": "{} {} not found".format(obj_name, uid)}


def test_patch_existing_project(client):  # TODO: Test whenever name is not changed.
    post_response = client.post(base_url, json=example_project, headers=api_key_header)
    overwritejson = copy.deepcopy(post_response.json)
    overwritejson["title"] = "something else"


    response = client.patch(base_url + post_response.json["_id"], json={"title": overwritejson["title"]}, headers=api_key_header)

    assert response.status_code == 200
    assert response.json == overwritejson
