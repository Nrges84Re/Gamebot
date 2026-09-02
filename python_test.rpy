init python:

    import sys
    import os

    PYTHON_ENGINE_PATH = os.path.join(
        config.basedir,
        "python_engine"
    )

    if PYTHON_ENGINE_PATH not in sys.path:
        sys.path.append(PYTHON_ENGINE_PATH)