from pathlib import Path

from pydantic import BaseModel


def write_log(contents: str, path: Path) -> None:
    with open(path, "w") as f:
        f.write(contents)


class OpenFoldResult(BaseModel):
    """Return result from the OpenFold funcX endpoint."""

    returncode: int
    """Return code of the OpenFold job."""
    stdout: str
    """Standard out of the OpenFold job."""
    stderr: str
    """Standard error of the OpenFold job."""
