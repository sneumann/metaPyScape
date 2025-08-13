#!/usr/bin/env python3

"""
UsingMetaPyScape
"""

import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint
import yaml
import json

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
# Reading the configuration from config.yml with keys base_path and api-key

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

configuration = metaPyScape.Configuration(
    host = config.get("base_path", "http://localhost"),
)

# Enter a context with an instance of the API client
with metaPyScape.ApiClient(configuration, 
                           header_name="api-key", 
                           header_value=config.get("api-key", None)) as api_client:
    projects_api = metaPyScape.ProjectsApi(api_client)

    try:
        api_response = projects_api.list_all_projects()
        # print as JSON
        print(json.dumps(api_response, default=str, indent=2))
    except ApiException as e:
        print("Exception when calling Project->list_all_projects: %s\n" % e)