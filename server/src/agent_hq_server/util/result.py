"""Issue/Result helpers: content problems are non-fatal and collectable."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


class ContentError(Exception):
    """A content file could not be parsed or validated."""


@dataclass(frozen=True)
class Issue:
    """A non-fatal content problem (surfaced by `agent-hq validate` later)."""

    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


@dataclass
class Result(Generic[T]):
    """A produced value plus any non-fatal issues collected along the way."""

    value: T | None = None
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.value is not None

    def add_issue(self, path: str, message: str) -> None:
        self.issues.append(Issue(path=path, message=message))

    def expect(self, label: str) -> T:
        """Return the value, or raise a ContentError listing all issues."""
        if self.value is None:
            detail = "; ".join(issue.render() for issue in self.issues) or "no value"
            raise ContentError(f"{label} failed: {detail}")
        return self.value
