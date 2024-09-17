#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    
    os.environ["GooglePalmAPIKey"] = "enter API Key here"

    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    ENDPOINT_URI = os.environ.get("GoogleAIServiceEndpoint", "")
    API_KEY = os.environ.get("GooglePalmAPIKey", "")
    print(f"ENDPOINT_URI = {ENDPOINT_URI}, API_KEY = {API_KEY}")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "")
