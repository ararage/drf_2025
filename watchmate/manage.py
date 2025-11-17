#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    # Ensure project root is on PYTHONPATH so top-level packages (e.g. `config`)
    # are importable when the project is mounted into the container at /app.
    current_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_path)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Also add the inner application directory for backwards-compatibility.
    inner_apps = os.path.join(current_path, "watchmate")
    if inner_apps not in sys.path:
        sys.path.append(inner_apps)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    """Run administrative tasks."""
    from django.conf import settings

    print(settings)

    if settings.DEBUG:
        if os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN"):
            import ptvsd

            print("Waiting for debugger attach...")
            ptvsd.enable_attach(address=("0.0.0.0", 3000))
            ptvsd.wait_for_attach()
            print("Attached!")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # previous sys.path insertion moved earlier to ensure imports work

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
