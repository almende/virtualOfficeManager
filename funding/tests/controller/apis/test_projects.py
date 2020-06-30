import copy

api_version = "v1"
base_url = '/api/{}/projects/'.format(api_version)

# The following contains only the required fields
example_project = {"title": "x", "description": "dx", "programme": "px", "project_id": "pidx", "source": "sx"}
obj_name = "project"
api_key_header = {'X-API-KEY': 'fake key'}


def remove_ids(json):
    json = copy.deepcopy(json)
    for o in json:
        del o["id"]

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
    example_project_2 = example_project.copy()
    example_project_2["title"] = "y"

    data = [example_project,example_project_2]
    client.post(base_url, json=data[0], headers=api_key_header)
    client.post(base_url, json=data[1], headers=api_key_header)
    response = client.get(base_url)

    assert response.status_code == 200
    assert remove_ids(response.get_json()) == data


def test_post_project_ok(client):
    response = client.post(base_url, json=example_project, headers=api_key_header)

    assert response.status_code == 201
    assert remove_ids([response.get_json()])[0] == example_project


def test_post_project_missing_required_field(client):
    project_copy = example_project.copy()
    del project_copy["title"]
    response = client.post(base_url, json=project_copy, headers=api_key_header)

    assert response.status_code == 400
    assert response.get_json() == {'errors': {'title': "'title' is a required property"}, 'message': 'Input payload validation failed'}


def test_delete_existing_project(client):
    post_response = client.post(base_url, json=example_project, headers=api_key_header)

    response = client.delete(base_url + post_response.json["id"], headers=api_key_header)

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


    response = client.patch(base_url + post_response.json["id"], json={"title": overwritejson["title"]}, headers=api_key_header)

    assert response.status_code == 200
    assert response.json == overwritejson
