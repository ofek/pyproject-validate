from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Validator(ABC):
    def __init__(self):
        self.fixable = True

    @abstractmethod
    def validate(self, data: Dict[str, Any], errors: List[str], warnings: List[str]):
        """
        Validates the provided raw deserialized pyproject.toml `data`. If any errors cannot
        be automatically fixed, set `self.fixable` to `False`.
        """

    @abstractmethod
    def fix(self, data: Dict[str, Any]):
        """
        Fixes the provided raw deserialized pyproject.toml `data`. This method will not be
        called if `self.fixable` is set to `False`.
        """


class SpecValidator(Validator):
    def validate(self, data, errors, warnings):
        # Slow import
        from .models import BuildSystemConfig, ProjectConfig

        try:
            BuildSystemConfig(**data.get("build-system", {}))
        except Exception as e:
            self.fixable = False
            errors.append(str(e))

        try:
            ProjectConfig(**data.get("project", {}))
        except Exception as e:
            self.fixable = False
            errors.append(str(e))

    def fix(self, data):  # no cov
        """
        Will never be called.
        """


class NameValidator(Validator):
    def __init__(self):
        super().__init__()

        self._name = ""

    def validate(self, data, errors, warnings):
        name = data["project"].get("name")

        # Previous error
        if not isinstance(name, str):
            return

        # https://www.python.org/dev/peps/pep-0508/#names
        if not re.search("^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", name, re.IGNORECASE):
            self.fixable = False
            errors.append("must only contain ASCII letters/digits, underscores, hyphens, and periods")
            return

        # https://www.python.org/dev/peps/pep-0503/#normalized-names
        self._name = re.sub(r"[-_.]+", "-", name).lower()

        if name != self._name:
            errors.append(f"should be {self._name}")

    def fix(self, data):
        data["project"]["name"] = self._name


def get_validators():
    # allow choices one day
    return {"specs": SpecValidator(), "naming": NameValidator()}
