from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Handler(ABC):
    def __init__(self, path: Optional[str] = None):
        self._path = path

    @property
    def path(self):
        if self._path is None:
            root = os.getcwd()
            while True:
                path = os.path.join(root, "pyproject.toml")
                if os.path.isfile(path):
                    self._path = path
                    break

                new_root = os.path.dirname(root)
                if new_root == root:
                    raise OSError("could not locate a `pyproject.toml` file")

                root = new_root

        return self._path

    def read(self) -> str:
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def write(self, text: str):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        Deserializes the pyproject.toml file.
        """

    @abstractmethod
    def save(self, data: Dict[str, Any]):
        """
        Serializes the `data` to the pyproject.toml file.
        """


class StandardHandler(Handler):
    def load(self):
        import tomli

        return tomli.loads(self.read())

    def save(self, data):
        import tomli_w

        self.write(tomli_w.dumps(data))


def get_handler(path: Optional[str] = None):
    # comment-preserving version one day
    return StandardHandler(path)
