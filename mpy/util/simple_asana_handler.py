# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

"""
Simple handler for building application-specific Asana requests
and sending them to the simple API
"""

import gc
import sys

import mpy.secrets as secrets
import mpy.util.simple_asana_api as api
import mpy.hal.config as cfg

IS_LINUX = (sys.platform == 'linux')

if not IS_LINUX:
    import mpy.networking.wifi as wifi

class Simple_asana_handler:
    """
    Simple wrapper for sending HTTP requests to Asana API
    """
    token = ''
    brew_project_gid = ''
    active_task_gid = ''
    jwt_task_gid = ''
    exception_log_task_gid = ''

    # Names of important projects and tasks
    PROJECT_NAME_BREW = 'Closet Brewing'
    WORKSPACE_NAME = 'Personal Projects'
    TASK_NAME_SANDBOX = 'Hydra sandbox'
    TASK_NAME_JWT_STORE = 'Hydra Gsheets JWT Store'
    TASK_NAME_EXCEPTION_LOG = 'Hydra exception log'

    # Mapping between Asana section names and app that should handle them
    app_map = {
        'Planned': 'coldcrash_tracker',
        'In Primary': 'fermentation_tracker',
        'In Secondary': 'fermentation_tracker'
    }

    def __init__(self, token=None, active_task=None, active_subtask=None):
        # Figure out which machine we are running on
        if IS_LINUX:
            self.name = cfg.HYDRA_NAME_MAP['unix']
        else:
            self.name = cfg.HYDRA_NAME_MAP[wifi.MAC]

            # Make sure we're connected
            wifi.connect_with_retry()

        # Store personal access token
        if token:
            self.token = token
        else:
            self.token = secrets.get_secrets()[f'asana_personal_access_token_{self.name}']

        # Fetch and store brewing project GID
        self.brew_project_gid = self.get_personal_project_gid_by_name(self.PROJECT_NAME_BREW)

        # Fetch and store relevant task GIDs
        if active_task:
            self.active_task_gid = active_task
        else:
            self.active_task_gid = self.get_sandbox_task_gid()
        if active_subtask:
            self.active_subtask_gid = active_subtask
        else:
            self.active_subtask_gid = self.get_sandbox_task_gid()

        self.jwt_task_gid = self.get_task_gid_by_name(self.TASK_NAME_JWT_STORE)
        self.exception_log_task_gid = self.get_task_gid_by_name(self.TASK_NAME_EXCEPTION_LOG)

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
        Returns False if failed to fetch it
        """
        # Get personal projects workspace
        pp_gid = self.get_personal_projects_gid()

        # Get all the projects in that workspace
        projects = api.get_projects_for_workspace(workspace_gid=pp_gid, token=self.token)

        if not projects:
            return False

        # Get and return the specified project
        target_project = next(project for project in projects if project['name'] == name)
        return target_project['gid']

    def get_task_gid_by_name(self, name):
        """
        Returns the gid for the named task
        Returns False if failed to fetch it
        """
        tasks = api.get_tasks_for_project(project_gid=self.brew_project_gid, token=self.token)

        if not tasks:
            return False

        # Get and return specified task
        named_task = next(task for task in tasks if task['name'] == name)
        return named_task['gid']

    def get_sandbox_task_gid(self):
        """
        Returns the gid for the active task
        Returns False if failed to fetch it
        """
        # TODO: Find a way to figure out which task is active for coldcrash or fermentation.
        # Maybe magic section in Asana to read from
        return self.get_task_gid_by_name(self.TASK_NAME_SANDBOX)

    def get_active_task_description(self):
        """
        Returns the description on the active task
        """
        return api.get_task(task_gid=self.active_task_gid, token=self.token, fields=['notes'])['notes']

    def update_active_task_description(self, desc):
        """
        Updates the description on the active task with user specified string desc
        """
        params = {
            'notes': desc
        }
        if not self.active_task_gid:
            self.active_task_gid = self.get_sandbox_task_gid()

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
        if not self.active_task_gid:
            self.active_task_gid = self.get_sandbox_task_gid()
        return api.add_comment_on_task(task_gid=self.active_task_gid, token=self.token, params=params)

    def add_comment_on_active_subtask(self, text, is_pinned=False):
        """
        Adds a comment on the active subtask with user specified string text. 
        Will pin to top of subtask if is_pinned is True.
        """
        params = {
            "is_pinned": is_pinned,
            "text": text
        }
        if not self.active_subtask_gid:
            self.active_subtask_gid = self.get_sandbox_subtask_gid()
        return api.add_comment_on_task(task_gid=self.active_subtask_gid, token=self.token, params=params)

    def get_jwt(self):
        """
        Get the latest JWT
        """
        if not self.jwt_task_gid:
            self.jwt_task_gid = self.get_task_gid_by_name(self.TASK_NAME_JWT_STORE)

        gc.collect()
        r = api.get_task(task_gid=self.jwt_task_gid, token=self.token)

        return r['notes']

    def put_jwt(self, jwt):
        """
        Put the given JWT
        """
        params = {
            'notes': jwt
        }
        if not self.jwt_task_gid:
            self.jwt_task_gid = self.get_task_gid_by_name(self.TASK_NAME_JWT_STORE)
        return api.update_task(task_gid=self.jwt_task_gid, token=self.token, params=params)

    def update_exception_log(self, msg):
        """
        Add a comment to the exception log
        """
        params = {
            "text": msg
        }
        if not self.exception_log_task_gid:
            self.exception_log_task_gid = self.get_sandbox_task_gid()
        return api.add_comment_on_task(task_gid=self.exception_log_task_gid, token=self.token, params=params)

    def get_section_gid_by_name(self, name):
        """
        Returns the gid for the named task
        Returns False if failed to fetch it
        """
        tasks = api.get_sections_for_project(project_gid=self.brew_project_gid, token=self.token)

        if not tasks:
            return False

        # Get and return specified task
        active_task = next(task for task in tasks if task['name'] == name)
        return active_task['gid']

    def get_tasks_for_section(self, section_gid):
        """
        Returns a list of tasks in the specified section
        """
        return api.get_tasks_for_section(section_gid, self.token)

    def get_subtasks_for_task(self, task_gid):
        """
        Returns a list of subtasks in the specified task
        """
        return api.get_subtasks_for_task(task_gid, self.token)

    def find_assigned_subtask_in_section(self, section_name):
        """
        Finds a subtask assigned to authenticated user in the named section.
        Returns the first match, or None if no matches
        """
        section_gid = self.get_section_gid_by_name(section_name)
        tasks = self.get_tasks_for_section(section_gid)

        for task in tasks:
            subtasks = self.get_subtasks_for_task(task['gid'])

            for subtask in subtasks:
                subtask_info = api.get_task(subtask['gid'], self.token, fields=['assignee'])
                try:
                    assignee = subtask_info['assignee']['name']
                    if assignee == self.name:
                        return (subtask['gid'], task['gid'], task['name'])
                except TypeError:
                    pass

        return None

    def decide_on_app(self):
        """
        Decides on which app should be run.
        Does this by checking for any subtasks in the specified
        section that are assigned to the authenticated user.
        If found:
            Returns tuple of app, subtask_gid, task_name
        If none found, returns None.
        """
        for section, app in self.app_map.items():
            r = self.find_assigned_subtask_in_section(section)
            if r:
                subtask_gid, task_gid, task_name = r
                api.add_comment_on_task(task_gid=subtask_gid, token=self.token, params={'text': 'On it!'})
                if app == 'fermentation_tracker':
                    mode = section.split('In ')[1]
                else:
                    mode = section
                return (app, mode, subtask_gid, task_gid, task_name)

        return None