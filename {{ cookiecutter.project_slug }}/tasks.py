import dataclasses
import pathlib

import invoke

#############
# CONSTANTS #
#############

PACKAGE = "{{ cookiecutter.project_slug }}"

###################
# GETTING STARTED #
###################


@invoke.task
def help(ctx):
    """
    Displays help text
    """
    ctx.run("inv -l", pty=True)


@invoke.task()
def install(ctx, skip_install_playwright: bool = False):
    """
    Install system dependencies necessary for the {{ cookiecutter.project_name }} project.

    This task optionally skips the installation of Playwright dependencies,
    which is useful for CI pipelines where Playwright is not needed,
    thereby improving the build performance.
    """
    _title("Installing Dependencies")
    ctx.run("uv sync")

    if not skip_install_playwright:
        _title("Installing Playwright Dependencies")
        ctx.run("uv run playwright install --with-deps")


#####################
# QUALITY ASSURANCE #
#####################


@invoke.task
def format(ctx, check: bool = False) -> None:  # noqa: A001
    """
    Apply automatic code formatting tools

    By default, this modifies files to match coding style guidelines.
    When `check` is True, it performs a dry-run to identify non-compliant
    files without applying changes.
    """
    suffix = " (check only)" if check else ""
    _title(f"Applying code formatters{suffix}")
    ctx.run(f"uv run ruff format src{' --check' if check else ''}")
    ctx.run(f"uv run ruff check --select I{' --fix' if not check else ''} src")


@invoke.task
def typing(ctx):
    """
    Check type annotations
    """
    _title("Type checking")
    # PYTHONPATH must include the `src` folder for django-stubs to find the settings
    # module
    src_path = str((pathlib.Path() / "src").absolute())
    with ctx.prefix(
        f"export PYTHONPATH={% raw %}${{PYTHONPATH}}{% endraw %}:{src_path}"
    ):
        try:
            ctx.run(f"uv run dmypy run -- src/{PACKAGE}")
        except invoke.exceptions.UnexpectedExit:
            print(
                "\n"
                "NOTE: mypy was run in daemon mode, which can lead to spurious\n"
                "errors when changing branches.\n"
                "If the errors observed do not make sense, or errors are occuring\n"
                "on known-good code run `inv typing-daemon-stop` to stop the\n"
                "dmypy daemon and run type checking again."
            )
            raise


@invoke.task
def typing_daemon_stop(ctx):
    """
    Stop the mypy typing daemon

    Sometimes dmypy gets itself confused and needs to be stopped
    """
    _title("Terminating type checking Daemon")
    ctx.run("uv run dmypy stop")


@invoke.task
def lint(ctx, fix=False):
    """
    Check linting in the src folder
    """
    _title(f"Linting code {'' if fix else '(check only)'}")
    ctx.run(f"uv run ruff check{' --fix ' if fix else ''} src")



@invoke.task
def check_migrations(ctx):
    """
    Check for potential vulnerabilities in packages
    """
    _title("Checking for missing migrations")
    try:
        ctx.run(
            f"uv run ./src/{PACKAGE}/manage.py makemigrations --dry-run --check",
            pty=True,
        )
    except invoke.exceptions.UnexpectedExit:
        print(
            "\n"
            "There are model changes with no migrations generated for them. "
            f"Run `./src/{PACKAGE}/manage.py makemigrations` to generate migrations, "
            "and don't forget to commit the new migration files!"
        )
        raise


@invoke.task(
    help={
        "name": "only run tests which match the keyword expression",
        "suite": "Only run tests in the named suite (system|functional)",
        "verbose": "run tests in verbose mode",
    }
)
def test(ctx, name="", verbose=False, suite=None):
    """
    Runs the test suite
    """
    title_suffix = "S"
    args = ["uv run pytest"]
    if verbose:
        args.append("-vv")

    if suite:
        args += ["-m", suite]
        title_suffix = f" ({suite})"
    if name:
        args += ["--no-cov", "-sk", name]
    else:
        args += [
            f"--cov={PACKAGE}",
            "--cov-report=term",
            "--cov-report=xml",
            "--no-cov-on-fail",
            "--cov-context=test",
        ]

    args.append("src/tests")

    cmd = " ".join(args)
    _title(f"Running the test suite{title_suffix} ✅")
    ctx.run(cmd, pty=True, echo=True)
    if "--cov" in cmd:
        ctx.run("uv run coverage html --show-contexts")


@invoke.task(typing, test, lint, check_migrations)
def check(ctx):
    """
    Runs all the code checking tools
    """
    print("All checks completed successfully 🕺")


############
# BUILDING #
############


@invoke.task
def build_image(ctx, tag=None, pty=True):
    """
    Build the service Docker image
    """
    _title("Building Docker image 🐳")
    commit_hash = "N/A"
    commit_time = "N/A"
    commit_count = -1

    if tag is None:
        data = _build_data(ctx)
        commit_hash = data.commit_hash
        commit_time = data.commit_time
        commit_count = data.commit_count
        tag = data.tag

    ctx.run(
        "docker build "
        f"--build-arg GIT_COMMIT_HASH={commit_hash} "
        f"--build-arg GIT_COMMIT_TIME={commit_time} "
        f"--build-arg GIT_COMMIT_COUNT={commit_count} "
        f"-t {PACKAGE}:{tag} .",
        pty=pty,
        echo=True,
    )


@invoke.task
def build_docs(ctx):
    """
    Build the {{ cookiecutter.project_name }} documentation
    """
    _title("Building documentation")
    ctx.run("uv run mkdocs build --strict")


###########
# RUNNING #
###########


@invoke.task
def run_image(
    ctx,
    tag: str | None = None,
    network: str | None = None,
    env_file: str | None = None,
    database_url: str | None = None,
    command: str | None = None,
):
    """
    Run the service Docker image

    Alternatively execute input commands in the container.
    """
    _title("Running Docker image 🐳")

    tag = tag or _build_data(ctx).tag
    network = network or f"{PACKAGE}_default"
    env_file = env_file or ".env"
    database_url = database_url or "postgres://dev:dev_password@db:5432/dev"

    args = [
        "docker run",
        "--rm",
        "-it",
        "-p 8000:8000",
        f"--network {network}",
        f"-e DATABASE_URL={database_url}",
        f"--env-file {env_file}",
        f"{PACKAGE}:{tag}",
    ]

    if command:
        args.append(command)

    ctx.run(" ".join(args), echo=True, pty=True)


@invoke.task
def run_docs(ctx):
    """
    Run the {{ cookiecutter.project_name }} documentation locally
    """
    ctx.run("uv run mkdocs serve")


###########
# HELPERS #
###########
def _title(text):
    print(f"== {text.upper()} ==")


@dataclasses.dataclass
class BuildData:
    MAX_TAG_LENGTH = 128

    branch: str
    commit_hash: str
    commit_time: str
    commit_count: str

    @property
    def tag(self) -> str:
        max_branch_length = self.MAX_TAG_LENGTH - (
            len(self.commit_count) + 1
        )  # 1 for the hyphen
        return "-".join([self.branch[:max_branch_length], self.commit_count])


def _build_data(ctx) -> BuildData:
    """
    Retrieves the current git branch, commit hash and commit time for using during builds

    Also provides a `tag` which is suitable for use as a Docker image tag based on these values
    """
    max_tag_length = 128
    branch = ctx.run("git rev-parse --abbrev-ref HEAD", hide="stdout").stdout.strip()
    branch = (
        branch[:max_tag_length]
        .replace("/", "-")
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    commit_hash = ctx.run("git rev-parse --short=12 HEAD", hide="stdout").stdout.strip()
    commit_time = ctx.run("git show -s --format=%ct", hide="stdout").stdout.strip()
    commit_count = ctx.run("git rev-list --count HEAD", hide="stdout").stdout.strip()
    return BuildData(
        branch=branch,
        commit_hash=commit_hash,
        commit_time=commit_time,
        commit_count=commit_count,
    )
