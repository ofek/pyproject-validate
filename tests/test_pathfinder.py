import os


def test_missing(project_file, invoke):
    result = invoke()

    assert result.code == 1, result.output
    assert (
        result.output
        == """\
could not locate a `pyproject.toml` file
"""
    )


def test_current_directory(project_file, invoke):
    project_file.write(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
"""
    )

    result = invoke()

    assert result.code == 0, result.output
    assert not result.output


def test_parent_directory(project_file, invoke):
    project_file.write(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
"""
    )

    sub_directory = project_file.path.parent / "foo"
    sub_directory.mkdir()
    os.chdir(sub_directory)

    result = invoke()

    assert result.code == 0, result.output
    assert not result.output


def test_explicit_path(project_file, invoke):
    project_file.write(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
"""
    )

    sub_directory = project_file.path.parent / "foo"
    sub_directory.mkdir()
    path = sub_directory / "pyproject.toml"
    project_file.path.replace(path)

    result = invoke("--config", str(path))

    assert result.code == 0, result.output
    assert not result.output
