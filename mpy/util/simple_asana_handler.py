# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple handler for building application-specific Asana requests
and sending them to the simple API
"""

import mpy.secrets as secrets
import mpy.util.simple_asana_api as api

class Simple_asana_handler:
    """
    Simple wrapper for sending HTTP requests to Asana API
    """
    token = ''
    brew_project_gid = ''
    active_task_gid = ''
    jwt_task_gid = ''

    # Names of important projects and tasks
    PROJECT_NAME_BREW = 'Closet Brewing'
    WORKSPACE_NAME = 'Personal Projects'
    TASK_NAME_SANDBOX = 'Hydra sandbox'
    TASK_NAME_JWT_STORE = 'Hydra Gsheets JWT Store'

    def __init__(self):
        # Store personal access token
        self.token = secrets.get_secrets()['asana_personal_access_token']

        # Fetch and store brewing project GID
        self.brew_project_gid = self.get_personal_project_gid_by_name(self.PROJECT_NAME_BREW)

        # Fetch and store relevant task GIDs
        self.active_task_gid = self.get_active_task_gid()
        self.jwt_task_gid = self.get_task_gid_by_name(self.TASK_NAME_JWT_STORE)

    def get_personal_projects_gid(self):
        """
        Returns the gid for the personal projects workspace of the authenticated user
        """
        me = api.get_me(self.token)
        personal_projects = next(workspace for workspace in me['workspaces'] if workspace['name'] == self.WORKSPACE_NAME)
        return personal_projects['gid']

    def get_personal_project_gid_by_name(self, name):
        """
        Returns the gid for the personal project specified by name (string).
        """
        # Get personal projects workspace
        pp_gid = self.get_personal_projects_gid()

        # Get all the projects in that workspace
        projects = api.get_projects_for_workspace(workspace_gid=pp_gid, token=self.token)

        # Get and return the specified project
        target_project = next(project for project in projects if project['name'] == name)
        return target_project['gid']

    def get_task_gid_by_name(self, name):
        """
        Returns the gid for the named task
        """
        tasks = api.get_tasks_for_project(project_gid=self.brew_project_gid, token=self.token)

        # Get and return specified task
        active_task = next(task for task in tasks if task['name'] == name)
        return active_task['gid']

    def get_active_task_gid(self):
        """
        Returns the gid for the active task
        """
        # TODO: Find a way to figure out which task is active for coldcrash or fermentation.
        # Maybe magic section in Asana to read from
        return self.get_task_gid_by_name(self.TASK_NAME_SANDBOX)

    def update_active_task_description(self, desc):
        """
        Updates the description on the active task with user specified string desc
        """
        params = {
            'notes': desc
        }
        return api.update_task(task_gid=self.active_task_gid, token=self.token, params=params)

    def add_comment_on_active_task(self, text, is_pinned=False):
        """
        Adds a comment on the active task with user specified string text. 
        Will pin to top of task if is_pinned is True.
        """
        params = {
            "is_pinned": is_pinned,
            "text": text
        }
        return api.add_comment_on_task(task_gid=self.active_task_gid, token=self.token, params=params)

    def get_jwt(self):
        """
        Get the latest JWT
        """
        return api.get_task(task_gid=self.jwt_task_gid, token=self.token)['notes']