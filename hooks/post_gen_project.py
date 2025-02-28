import pathlib
import secrets


PROJECT_ROOT = pathlib.Path()


def main():
    _set_secret_key()


def _set_secret_key():
    """
    Generate a random secret key and replace the placeholder in the example.env file
    """
    secret_key = "".join(
        secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)")
        for i in range(50)
    )
    with (PROJECT_ROOT / "example.env").open("r+") as f:
        file_contents = f.read().replace("!!!DJANGO_SECRET_KEY!!!", secret_key)
        f.seek(0)
        f.write(file_contents)
        f.truncate()


if __name__ == "__main__":
    main()
