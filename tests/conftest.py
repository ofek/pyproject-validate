import os
import sys
from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from pyproject_validate.cli import main

InvocationResult = namedtuple("InvocationResult", ["code", "output"])


class ProjectFile:
    def __init__(self, directory: Path):
        self.directory = directory
        self.path = directory / "pyproject.toml"

    def read(self) -> str:
        return self.path.read_text(encoding="utf-8")

    def write(self, text: str):
        self.path.write_text(text, encoding="utf-8")


def _invoke(args, capsys):
    with pytest.raises(SystemExit) as e:
        original_sys_argv = sys.argv
        try:
            sys.argv = ["pyproject-validate", *args]
            main()
        finally:
            sys.argv = original_sys_argv

    return InvocationResult(e.value.code, "".join(capsys.readouterr()))


@pytest.fixture
def invoke(capsys):
    return lambda *args: _invoke(args, capsys)


@pytest.fixture
def project_file():
    with TemporaryDirectory() as d:
        path = Path(d).resolve()
        origin = os.getcwd()

        try:
            os.chdir(path)
            yield ProjectFile(path)
        finally:
            os.chdir(origin)
