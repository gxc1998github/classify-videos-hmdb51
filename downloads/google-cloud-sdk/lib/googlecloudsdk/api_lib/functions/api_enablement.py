# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for enabling service APIs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from typing import Optional

from googlecloudsdk.api_lib.services import enable_api
from googlecloudsdk.api_lib.services import exceptions
from googlecloudsdk.api_lib.util import api_enablement
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io


def PromptToEnableApiIfDisabled(
    service_name: str, enable_by_default: Optional[bool] = False
):
  """Prompts to enable the API if it's not enabled.

  Args:
    service_name: The name of the service to enable.
    enable_by_default: default choice for the enablement prompt.
  """
  project_id = properties.VALUES.core.project.GetOrFail()
  try:
    if enable_api.IsServiceEnabled(project_id, service_name):
      return

    if console_io.CanPrompt():
      api_enablement.PromptToEnableApi(
          project_id, service_name, enable_by_default=enable_by_default
      )
    else:
      log.warning(
          "Service {} is not enabled. This operation may not succeed.".format(
              service_name
          )
      )
  except exceptions.GetServicePermissionDeniedException:
    log.info(
        "Could not verify if service {} is enabled: missing permission"
        " 'serviceusage.services.get'.".format(service_name)
    )
