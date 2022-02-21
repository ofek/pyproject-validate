class TestInvalidCharacters:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo bar"
version = "0.0.1"
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< naming >>>
error: must only contain ASCII letters/digits, underscores, hyphens, and periods
"""
        )

    def test_cannot_fix(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke("--fix")

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< naming >>>
error: must only contain ASCII letters/digits, underscores, hyphens, and periods
"""
        )


class TestNormalization:
    BEFORE = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "Foo.bAr"
version = "0.0.1"
"""
    AFTER = """\
[build-system]
requires = [
    "hatchling",
]
build-backend = "hatchling.build"

[project]
name = "foo-bar"
version = "0.0.1"
"""

    def test_error(self, project_file, invoke):
        project_file.write(self.BEFORE)

        result = invoke()

        assert result.code == 1, result.output
        assert (
            result.output
            == """\
<<< naming >>>
error: should be foo-bar
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
