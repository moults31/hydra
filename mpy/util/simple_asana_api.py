# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple stateless wrapper for sending HTTP requests to Asana API.
Exposes only the endpoints required for hydra's applications.
Only supports personal access token authentication, not client authentication.
"""

try:
    import urequests as requests
except:
    import requests

ENDPOINT_BASE = "https://app.asana.com/api/1.0"
ENDPOINT_ME = "https://app.asana.com/api/1.0/users/me"

def exception_wrapper(func):
    """
    Decorator to prevent us from hanging when an exception is raised by urequests
    """
    def wrapper(*args, **kwargs):
        try:
            rv = func(*args, **kwargs)
            return rv
        except BaseException as e:
            print(f"WARNING: Ignoring exception thrown by {func.__name__}. Details:")
            print(e)
            return False
    return wrapper

def _build_header(token, content_type=None, accept=None):
    headers = {}

    if content_type:
        headers['Content-type'] = content_type

    if accept:
        headers['Accept'] = accept

    headers['Authorization'] = f'Bearer {token}'

    return headers

@exception_wrapper
def get_me(token):
    """
    Makes a get request for the personal access token owner's user info and prints the response
    """
    data = {}
    headers = _build_header(token)

    return requests.get(ENDPOINT_ME, data=data, headers=headers).json()['data']

@exception_wrapper
def get_projects_for_workspace(workspace_gid, token):
    """
    Makes a get request for the list of projects in the specified workspace
    """
    endpoint = ENDPOINT_BASE + f"/workspaces/{workspace_gid}/projects"
    data = {}
    headers = _build_header(token)

    return requests.get(endpoint, data=data, headers=headers).json()['data']

@exception_wrapper
def get_tasks_for_project(project_gid, token):
    """
    Makes a get request for the list of tasks in the specified project
    """
    endpoint = ENDPOINT_BASE + f"/projects/{project_gid}/tasks"
    data = {}
    headers = _build_header(token)

    return requests.get(endpoint, data=data, headers=headers).json()['data']

def update_task(task_gid, token, params):
    """
    Makes a put request to update the parameters of the specified task
    """
    endpoint = ENDPOINT_BASE + f"/tasks/{task_gid}"
    data = {
        'data': params
    }
    headers = _build_header(
        token, 
        content_type='application/json',
        accept='application/json'
    )

    return requests.put(endpoint, json=data, headers=headers).json()['data']

def get_task(task_gid, token, fields=None):
    """
    Makes a get request to get the parameters of the specified task
    """
    endpoint = ENDPOINT_BASE + f"/tasks/{task_gid}"
    headers = _build_header(
        token, 
        content_type='application/json',
        accept='application/json'
    )
    if fields:
        data = {
            'fields': fields
        }
        return requests.get(endpoint, json=data, headers=headers).json()['data']
    else:
        return requests.get(endpoint, headers=headers).json()['data']

def add_comment_on_task(task_gid, token, params):
    """
    Adds a comment to the task. It will be authored by the authenticated user.
    """
    endpoint = ENDPOINT_BASE + f"/tasks/{task_gid}/stories"
    data = {
        'data': params
    }
    headers = _build_header(
        token, 
        content_type='application/json',
        accept='application/json'
    )
    return requests.post(endpoint, json=data, headers=headers).json()['data']

def get_sections_for_project(project_gid, token):
    """
    Gets the list of sections in the specified project
    """
    endpoint = ENDPOINT_BASE + f"/projects/{project_gid}/sections"
    data = {}
    headers = _build_header(token)

    return requests.get(endpoint, data=data, headers=headers).json()['data']

def get_tasks_for_section(section_gid, token):
    """
    Gets the list of tasks in the specified section
    """
    endpoint = ENDPOINT_BASE + f"/sections/{section_gid}/tasks"
    data = {}
    headers = _build_header(token)

    return requests.get(endpoint, data=data, headers=headers).json()['data']

def get_subtasks_for_task(task_gid, token):
    """
    Gets the list of subtasks in the specified task
    """
    endpoint = ENDPOINT_BASE + f"/tasks/{task_gid}/subtasks"
    data = {}
    headers = _build_header(token)

    return requests.get(endpoint, data=data, headers=headers).json()['data']
