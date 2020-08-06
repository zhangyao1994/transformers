# coding=utf-8
# Copyright 2020 Optuna, Hugging Face
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Logging utilities. """

import logging
import threading
from typing import Optional


from logging import CRITICAL  # NOQA
from logging import DEBUG  # NOQA
from logging import ERROR  # NOQA
from logging import FATAL  # NOQA
from logging import INFO  # NOQA
from logging import WARN  # NOQA
from logging import WARNING  # NOQA
from logging import NOTSET  # NOQA

_lock = threading.Lock()
_default_handler: Optional[logging.Handler] = None


def _get_library_logger() -> logging.Logger:
    return logging.getLogger("transformers")


def _configure_library_logger():
    global _default_handler

    with _lock:
        if _default_handler:
            # This library has already configured the library root logger.
            return
        _default_handler = logging.StreamHandler()  # Set sys.stderr as stream.

        # Apply our default configuration to the library root logger.
        library_logger = _get_library_logger()
        library_logger.addHandler(_default_handler)
        library_logger.setLevel(logging.WARN)
        library_logger.propagate = False


def get_verbosity() -> int:
    _configure_library_logger()
    return _get_library_logger().getEffectiveLevel()


def set_verbosity(verbosity: int) -> None:
    _configure_library_logger()
    _get_library_logger().setLevel(verbosity)


def get_logger():
    _configure_library_logger()
    return _get_library_logger()
