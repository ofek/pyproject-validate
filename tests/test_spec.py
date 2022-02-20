class TestBuildSystem:
    def test_requires_missing(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for BuildSystemConfig
requires
  field required (type=value_error.missing)
"""
        )

    def test_requires_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = "hatchling"
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for BuildSystemConfig
requires
  value is not a valid list (type=type_error.list)
"""
        )

    def test_build_backend_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = []

[project]
name = "foo"
version = "0.0.1"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for BuildSystemConfig
build-backend
  str type expected (type=type_error.str)
"""
        )

    def test_backend_path_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
backend-path = "."

[project]
name = "foo"
version = "0.0.1"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for BuildSystemConfig
backend-path
  value is not a valid list (type=type_error.list)
"""
        )


class TestAuthors:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
authors = [
    { name = "U.N. Owen", email = "void@some.where" },
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
authors = [
    { name = [9000], email = [] },
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
authors -> 0 -> email
  str type expected (type=type_error.str)
authors -> 0 -> name
  str type expected (type=type_error.str)
"""
        )


class TestClassifiers:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: Implementation :: CPython",
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
classifiers = [
    "Development Status :: 4 - Beta",
    [],
    "Programming Language :: Python :: Implementation :: CPython",
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
classifiers -> 1
  str type expected (type=type_error.str)
"""
        )


class TestDependencies:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "foo",
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "foo",
    [],
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
dependencies -> 1
  str type expected (type=type_error.str)
"""
        )


class TestDescription:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
description = "foo"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
description = []
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
description
  str type expected (type=type_error.str)
"""
        )


class TestDynamic:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dynamic = [
    "foo",
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dynamic = [
    "foo",
    [],
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
dynamic -> 1
  str type expected (type=type_error.str)
"""
        )

    def test_name(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dynamic = [
    "name",
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
dynamic
  the `name` field must not be listed as dynamic (type=value_error)
"""
        )

    def test_redefined(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
description = "foo"
dynamic = [
    "description",
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
__root__
  field(s) defined but also listed as dynamic: description (type=value_error)
"""
        )


class TestEntryPoints:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.entry-points.foo]
bar = "baz"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.entry-points.foo]
bar = []
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
entry-points -> foo -> bar
  str type expected (type=type_error.str)
"""
        )


class TestGUIScripts:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.gui-scripts]
foo = "bar"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.gui-scripts]
foo = []
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
gui-scripts -> foo
  str type expected (type=type_error.str)
"""
        )


class TestKeywords:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
keywords = [
    "foo",
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
keywords = [
    "foo",
    [],
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
keywords -> 1
  str type expected (type=type_error.str)
"""
        )


class TestLicense:
    def test_valid_string(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
license = "foo"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_valid_table(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
license = { file = "LICENSE.txt" }
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
license = { file = "LICENSE.txt", text = "accepted" }
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
license
  str type expected (type=type_error.str)
license -> __root__
  cannot contain both a `file` and `text` field (type=value_error)
"""
        )


class TestLicenseFiles:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
license-files = { paths = ["LICENSE.txt"] }
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
license-files = { paths = "LICENSE.txt", globs = "LICENSES/*" }
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
license-files -> globs
  value is not a valid list (type=type_error.list)
license-files -> paths
  value is not a valid list (type=type_error.list)
"""
        )

    def test_empty(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
license-files = {}
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
license-files -> __root__
  must contain either a `globs` or `paths` field (type=value_error)
"""
        )


class TestMaintainers:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
maintainers = [
    { name = "U.N. Owen", email = "void@some.where" },
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
maintainers = [
    { name = [9000], email = [] },
]
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
maintainers -> 0 -> email
  str type expected (type=type_error.str)
maintainers -> 0 -> name
  str type expected (type=type_error.str)
"""
        )


class TestName:
    def test_missing(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
version = "0.0.1"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
name
  field required (type=value_error.missing)
"""
        )

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = []
version = "0.0.1"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
name
  str type expected (type=type_error.str)
"""
        )


class TestOptionalDependencies:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.optional-dependencies]
foo = [
    "bar",
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.optional-dependencies]
foo = "bar"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
optional-dependencies -> foo
  value is not a valid list (type=type_error.list)
"""
        )


class TestReadme:
    def test_valid_string(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
readme = "README.md"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_valid_table(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
readme = { file = "README", content-type = "text/plain" }
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
readme = { file = "README.md", text = "docs" }
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
readme
  str type expected (type=type_error.str)
readme -> __root__
  cannot contain both a `file` and `text` field (type=value_error)
"""
        )

    def test_invalid_content_type(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
readme = { file = "README.md", content-type = "foo" }
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
readme
  str type expected (type=type_error.str)
readme -> content-type
  must be one of: text/markdown, text/x-rst, text/plain (type=value_error)
"""
        )

    def test_invalid_extension(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
readme = "README"
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
readme
  must have one of the following extensions: .md, .rst, .txt (type=value_error)
"""
        )


class TestScripts:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.scripts]
foo = "bar"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.scripts]
foo = []
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
scripts -> foo
  str type expected (type=type_error.str)
"""
        )


class TestURLs:
    def test_valid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.urls]
foo = "bar"
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.urls]
foo = []
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 1 validation error for ProjectConfig
urls -> foo
  str type expected (type=type_error.str)
"""
        )


class TestVersion:
    def test_valid_dynamic(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
dynamic = [
    "version",
]
"""
        )

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output

    def test_invalid(self, project_file, invoke):
        project_file.write(
            """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = []
"""
        )

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< specs >>>
error: 2 validation errors for ProjectConfig
version
  str type expected (type=type_error.str)
__root__
  missing field(s): version (type=value_error)
"""
        )
