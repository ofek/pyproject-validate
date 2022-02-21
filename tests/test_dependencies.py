class TestDependenciesInvalid:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "foo",
    "",
    "bar^0.1",
    "baz",
]
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: dependencies #2: Parse error at "''": Expected W:(0-9A-Za-z)
error: dependencies #3: Parse error at "'^0.1'": Expected string_end
"""
        )

    def test_cannot_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: dependencies #2: Parse error at "''": Expected W:(0-9A-Za-z)
error: dependencies #3: Parse error at "'^0.1'": Expected string_end
"""
        )


class TestOptionalDependenciesInvalid:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "bar",
    "foo",
]

[project.optional-dependencies]
foo = [
    "foo",
    "",
    "bar^0.1",
    "baz",
]
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: optional `foo` dependencies #2: Parse error at "''": Expected W:(0-9A-Za-z)
error: optional `foo` dependencies #3: Parse error at "'^0.1'": Expected string_end
"""
        )

    def test_cannot_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: optional `foo` dependencies #2: Parse error at "''": Expected W:(0-9A-Za-z)
error: optional `foo` dependencies #3: Parse error at "'^0.1'": Expected string_end
"""
        )


class TestDependenciesNormalization:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "python-dateutil",
    "bAr.Baz[TLS]   >=1.2RC5",
    'Foo;python_version<"3.8"',
]
"""
    AFTER = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "bar-baz[tls]>=1.2rc5",
    "foo; python_version < '3.8'",
    "python-dateutil",
]
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: dependencies #2 should be: bar-baz[tls]>=1.2rc5
error: dependencies #3 should be: foo; python_version < '3.8'
"""
        )

    def test_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 0, result.output
        assert not result.output
        assert project_file.read() == self.AFTER

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output


class TestOptionalDependenciesNormalization:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "bar",
    "foo",
]

[project.optional-dependencies]
foo = [
    "python-dateutil",
    "bAr.Baz[TLS]>=1.2RC5",
    'Foo; python_version < "3.8"',
]
"""
    AFTER = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "bar",
    "foo",
]

[project.optional-dependencies]
foo = [
    "bar-baz[tls]>=1.2rc5",
    "foo; python_version < '3.8'",
    "python-dateutil",
]
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: optional `foo` dependencies #2 should be: bar-baz[tls]>=1.2rc5
error: optional `foo` dependencies #3 should be: foo; python_version < '3.8'
"""
        )

    def test_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 0, result.output
        assert not result.output
        assert project_file.read() == self.AFTER

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output


class TestDependenciesSorting:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "foo",
    "bar",
]
"""
    AFTER = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"
dependencies = [
    "bar",
    "foo",
]
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: dependencies are not sorted
"""
        )

    def test_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 0, result.output
        assert not result.output
        assert project_file.read() == self.AFTER

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output


class TestOptionalDependenciesSorting:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.optional-dependencies]
foo = [
    "foo",
    "bar",
]
"""
    AFTER = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.0.1"

[project.optional-dependencies]
foo = [
    "bar",
    "foo",
]
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< dependencies >>>
error: optional `foo` dependencies are not sorted
"""
        )

    def test_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 0, result.output
        assert not result.output
        assert project_file.read() == self.AFTER

        result = invoke()

        assert result.code == 0, result.output
        assert not result.output
