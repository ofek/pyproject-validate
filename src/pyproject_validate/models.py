from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator

# TODO: https://github.com/samuelcolvin/pydantic/issues/1098#issuecomment-1009762620


class LicenseTableLegacy(BaseModel):
    file: Optional[str]
    text: Optional[str]

    @root_validator(pre=True)
    def _pre_validation(cls, values):
        if "file" in values and "text" in values:
            raise ValueError("cannot contain both a `file` and `text` field")

        return values


class AuthorTable(BaseModel):
    email: Optional[str]
    name: Optional[str]


class LicenseFilesTable(BaseModel):
    globs: Optional[List[str]]
    paths: Optional[List[str]]

    @root_validator(pre=True)
    def _pre_validation(cls, values):
        if not ("globs" in values or "paths" in values):
            raise ValueError("must contain either a `globs` or `paths` field")

        return values


class ReadmeTable(BaseModel):
    charset: Optional[str]
    content_type: str = Field(alias="content-type")
    file: Optional[str]
    text: Optional[str]

    @root_validator(pre=True)
    def _pre_validation(cls, values):
        if "file" in values and "text" in values:
            raise ValueError("cannot contain both a `file` and `text` field")

        return values

    @validator("content_type")
    def _validate_content_type(cls, v, field):
        known_content_types = ("text/markdown", "text/x-rst", "text/plain")
        if v not in known_content_types:
            raise ValueError(f'must be one of: {", ".join(known_content_types)}')

        return v


class BuildSystemConfig(BaseModel):
    """
    https://www.python.org/dev/peps/pep-0517/#source-trees
    """

    backend_path: Optional[List[str]] = Field(alias="backend-path")
    build_backend: str = Field(alias="build-backend")
    requires: List[str]


class ProjectConfig(BaseModel):
    """
    https://www.python.org/dev/peps/pep-0621/#details
    """

    authors: Optional[List[AuthorTable]]
    classifiers: Optional[List[str]]
    dependencies: Optional[List[str]]
    description: Optional[str]
    dynamic: Optional[List[str]]
    entry_points: Optional[Dict[str, Dict[str, str]]] = Field(alias="entry-points")
    gui_scripts: Optional[Dict[str, str]] = Field(alias="gui-scripts")
    keywords: Optional[List[str]]
    license: Optional[Union[str, LicenseTableLegacy]]
    license_files: Optional[LicenseFilesTable] = Field(alias="license-files")
    maintainers: Optional[List[AuthorTable]]
    name: str
    optional_dependencies: Optional[Dict[str, List[str]]] = Field(alias="optional-dependencies")
    readme: Optional[Union[str, ReadmeTable]]
    scripts: Optional[Dict[str, str]]
    urls: Optional[Dict[str, str]]
    version: Optional[str]

    @validator("readme")
    def _validate_readme(cls, v, field):
        if not isinstance(v, str):
            return v

        known_extensions = (".md", ".rst", ".txt")
        if not v.lower().endswith(known_extensions):
            raise ValueError(f'must have one of the following extensions: {", ".join(known_extensions)}')

        return v

    @validator("dynamic", pre=False)
    def _validate_dynamic(cls, v, field):
        if v is not None and "name" in v:
            # this would fail later on in the redefined check but let's be explicit
            raise ValueError("the `name` field must not be listed as dynamic")

        return v

    @root_validator(pre=False)
    def _validate_dynamic_fields(cls, values):
        static_fields = dict(values)
        dynamic_fields = set(static_fields.pop("dynamic", None) or [])

        required_fields = ["version"]
        missing = [
            field for field in required_fields if static_fields.get(field) is None and field not in dynamic_fields
        ]
        if missing:
            raise ValueError(f'missing field(s): {", ".join(missing)}')

        redefined = [field for field, value in static_fields.items() if value is not None and field in dynamic_fields]
        if redefined:
            raise ValueError(f'field(s) defined but also listed as dynamic: {", ".join(redefined)}')

        return values
