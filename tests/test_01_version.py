# Import CliRunner and create a runner object.
# This runner is what will "invoke" or "call" your command line application.
# Source:
# https://typer.tiangolo.com/tutorial/testing/#import-and-create-a-clirunner

from importlib.metadata     import version
from typer.testing          import CliRunner

from aircrack_tui           import app


runner = CliRunner()



def test_app():
    # Get app version from src/aircrack_tui/__init__.py
    app_version_result = runner.invoke(app, ["--version"])
    assert app_version_result.exit_code == 0
    # Get PDM package version from pyproject.toml
    pdm_package_version = version('aircrack-tui')
    # Assert equal:
    # Should be something like '0.1.0' in 'aicrack-tui v0.1.0\n'
    assert pdm_package_version in app_version_result.stdout
