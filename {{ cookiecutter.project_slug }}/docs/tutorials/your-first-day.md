# Your First Day

So it is your first day on the project, where do you start? Here!

This tutorial will guide you through getting the project up and running as well as
making your first update to the code.

## Installing UV

This project uses [uv] for both dependency management and for installing and maintaining
Python itself. Installing uv on macOS or Linux is quite simple:

```shell
curl -LsSf https://astral.sh/uv/0.7.3/install.sh | sh
```

If you have any difficulties, take a look at the full
[uv installation instructions][uv-install]

## Preparing your Development Environment

In addition to uv, this project makes heavy use of [invoke][pyinvoke] for automating the
various processes you might need to do on a day to day basis. Whilst uv is used for
managing your virtual environment, it is handy to have invoke installed globally so you
do not need to prefix every call with `uv run invoke ...`. You can install it globally
with:

```shell
uv tool install invoke
```

From then on you should be able to just call `invoke ...` or even shorter, `inv ...` to
run invoke tasks.

## Checking out the project

Now that everything is prepared, you can get to checking out a copy of the project from
Github and completing the setup.

```shell
git clone git@github.com:{{ cookiecutter.github_org }}/{{ cookiecutter.project_slug }}.git
```

The change directory into your newly cloned copy of the source code and complete the set
up:

```shell
cd {{ cookiecutter.project_slug }}
```

Take the example configuration file and make a copy for your local development:

```shell
cp example.env .env
```

And then finally you can installed the project which will ensure the correct version of
Python is available as well as create the virtual environment and installs project
dependencies.

```shell
uv sync
```

You are now all set to make your first change!

## Making your first change

Your first change will be to add yourself to the list of humans who have worked on the
project!

This project uses a simple [trunk based][trunkbased] approach to developing features
with short lived feature branches. So your first step making a change should always be
to create a new feature branch.

Within a terminal opened at the root of this project type:

```shell
git checkout -b add_name_to_humans_txt
```

This will create a new branch for your change.

Your change will be in `src/templates/pages/humans.txt`. Open this file and add
yourself! There is at least one example in there already you can copy. If you don't feel
comfortable sharing your Github name or general location that is fine, you do not need
to provide them.

Once you have made your changes, we need to commit it:

```shell
git add src/templates/pages/humans.txt
git commit -m "Adds me to the list of humans involved in this project"
```

This will first _stage_ the change with the `git add` then _commit_ to the change with
the `git commit`. For day to day commits we would expect a little more detail in the
commit message, but for this first day the above message is fine.

Next we need to create a pull request so others can review and approve you change.

```shell
git push origin add_name_to_humans_txt
```

This will push your branch up to Github. You can then use the Github website itself to
create the pull request - note that output from the `git push` actually includes a link
to Github that will take you straight to the correct place to do this.

Please provide a description of the change you are making, why you are making it and
ideally some pointers for the reviewer that would allow them to double check the change
is acting as intended.

Now you wait. A team member will review your changes and assuming they are happy with it
approve the change. Once they do you can click the `merge` button and add your change to
the `main` branch.

You can view your change once deployed at `https://<hostname>/humans.txt`

!!! note

    As a second change, consider the tutorial you just completed. Were any of the steps
    unclear? Did anything just _not_ work? Create new branch from the `main` branch and
    update this tutorial with anything you think needs fixing up. You can find the source
    for this tutorial at `docs/tutorials/your-first-day.md`

<!-- Links -->

[pyinvoke]: https://www.pyinvoke.org/
[trunkbased]: https://trunkbaseddevelopment.com/
[uv]: https://docs.astral.sh/uv
[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
