from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .utils import normalize_project_name


class Validator(ABC):
    def __init__(self):
        self.fixable = True
        self.exit_early = False

    @abstractmethod
    def validate(self, data: Dict[str, Any], errors: List[str], warnings: List[str]):
        """
        Validates the provided raw deserialized pyproject.toml `data`. If any errors cannot
        be automatically fixed, set `self.fixable` to `False`. If any errors may interfere
        with subsequent validation, set `self.exit_early` to `True`.
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
            self.exit_early = True
            errors.append(str(e))

        try:
            ProjectConfig(**data.get("project", {}))
        except Exception as e:
            self.fixable = False
            self.exit_early = True
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
        name = data["project"]["name"]

        # https://www.python.org/dev/peps/pep-0508/#names
        if not re.search("^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", name, re.IGNORECASE):
            self.fixable = False
            errors.append("must only contain ASCII letters/digits, underscores, hyphens, and periods")
            return

        self._name = normalize_project_name(name)

        if name != self._name:
            errors.append(f"should be {self._name}")

    def fix(self, data):
        data["project"]["name"] = self._name


class DependencyValidator(Validator):
    def __init__(self):
        super().__init__()

        self._dependencies = []
        self._optional_dependencies = {}

    def validate(self, data, errors, warnings):
        project_data = data["project"]

        self._validate_dependencies(project_data, errors, warnings)
        self._validate_optional_dependencies(project_data, errors, warnings)

    def fix(self, data):
        if self._dependencies:
            data["project"]["dependencies"] = self._dependencies

        if self._optional_dependencies:
            data["project"]["optional-dependencies"] = self._optional_dependencies

    def _validate_dependencies(self, project_data, errors, warnings):
        dependencies = project_data.get("dependencies", [])

        self._dependencies = self._validate_dependency_list(dependencies, errors, warnings)

    def _validate_optional_dependencies(self, project_data, errors, warnings):
        optional_dependencies = project_data.get("optional-dependencies", {})

        normalized = {}
        for name, dependencies in optional_dependencies.items():
            normalized[name] = self._validate_dependency_list(
                dependencies, errors, warnings, message_prefix=f"optional `{name}` dependencies"
            )

        self._optional_dependencies = normalized

    def _validate_dependency_list(self, dependencies, errors, warnings, message_prefix="dependencies"):
        # Slow import
        from packaging.requirements import InvalidRequirement, Requirement

        temp_errors = []
        temp_warnings = []

        normalized_dependencies = []
        for i, dependency in enumerate(dependencies, 1):
            try:
                requirement = Requirement(dependency)
            except InvalidRequirement as e:
                temp_errors.append(f"{message_prefix} #{i}: {e}")
                self.fixable = False
            else:
                requirement.name = normalize_project_name(requirement.name)

                # All TOML writers use double quotes, so avoid escaping
                normalized_dependency = str(requirement).lower().replace('"', "'")

                if dependency != normalized_dependency:
                    temp_errors.append(f"{message_prefix} #{i} should be: {normalized_dependency}")

                normalized_dependencies.append(normalized_dependency)

        errors.extend(temp_errors)
        warnings.extend(temp_warnings)
        normalized_dependencies.sort()

        # No need to check sorting if there were errors
        if temp_errors:
            return normalized_dependencies
        elif dependencies != normalized_dependencies:
            errors.append(f"{message_prefix} are not sorted")

        return normalized_dependencies


def get_validators():
    # allow choices one day
    return {"specs": SpecValidator(), "naming": NameValidator(), "dependencies": DependencyValidator()}
