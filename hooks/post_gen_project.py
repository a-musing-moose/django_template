import pathlib

PROJECT_ROOT = pathlib.Path()

def main():
    secret_key = "1234.567"
    _set_secret_key(secret_key)



def _set_secret_key(secret_key):

    with (PROJECT_ROOT / "example.env").open("r+") as f:
        file_contents = f.read().replace("!!!DJANGO_SECRET_KEY!!!", secret_key)
        f.seek(0)
        f.write(file_contents)
        f.truncate()


if __name__ == "__main__":
    main()
