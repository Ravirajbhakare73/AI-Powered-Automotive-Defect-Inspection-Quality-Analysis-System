import os


def get_project_root():

    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )


def ensure_directory(
    directory_path
):

    os.makedirs(
        directory_path,
        exist_ok=True
    )