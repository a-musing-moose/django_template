def main():
    _assert_valid_project_slug()


def _assert_valid_project_slug():
    """
    Ensure that the project slug is usable as a package identifier
    """
    project_slug = "{{ cookiecutter.project_slug }}"
    if hasattr(project_slug, "isidentifier"):
        assert (
            project_slug.isidentifier()
        ), f"{project_slug} is not a valid Python identifier."


if __name__ == "__main__":
    main()
