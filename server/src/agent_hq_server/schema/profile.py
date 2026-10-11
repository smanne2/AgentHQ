"""Profile — pure YAML; maps a detected stack to default content (technical.md §4.5)."""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*")


class FileMatch(BaseModel):
    """A matching rule against a project manifest file (technical.md §4.5).

    ``file`` is matched by basename against the signals mapping; when
    ``contains_any`` is set, at least one needle must appear in the text.
    """

    model_config = ConfigDict(extra="allow")

    file: str
    contains_any: list[str] | None = None


class Matches(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=(), populate_by_name=True)

    any_of: list[FileMatch] = Field(default_factory=list, alias="anyOf")
    all_of: list[FileMatch] = Field(default_factory=list, alias="allOf")


class Defaults(BaseModel):
    """Content the profile pins for every project that matches it."""

    model_config = ConfigDict(extra="allow")

    workflow: str | None = None
    roles: list[str] = Field(default_factory=list)
    instructions: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)


class Profile(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = ""
    matches: Matches | None = None
    stack: list[str] = Field(default_factory=list)
    defaults: Defaults = Field(default_factory=Defaults)

    @field_validator("id")
    @classmethod
    def _kebab_id(cls, value: str) -> str:
        if not _ID_PATTERN.fullmatch(value):
            raise ValueError("profile id must be kebab-case, e.g. 'node-web'")
        return value
