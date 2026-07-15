"""Tiny service used by the governance framework demo consumer."""


def describe_release(name: str, version: str) -> dict[str, str]:
    """Return a small release descriptor for tests and demo evidence."""
    if not name.strip():
        raise ValueError("name must not be empty")
    if not version.strip():
        raise ValueError("version must not be empty")

    return {
        "name": name,
        "version": version,
        "status": "demo",
    }
