#!/usr/bin/env python3
"""Validate the generated blueprints.

Usage, from the repository root::

    python3 scripts/check_blueprints.py

A blueprint repository has no unit tests, but it has the same failure mode as
any generated set: one language drifting away from the others, or a broken
template shipping unnoticed because nothing parses it before Home Assistant
does. This is what stands in for a test suite.

It checks that every file:
  * parses as YAML, `!input` included;
  * declares the keys Home Assistant requires;
  * exposes exactly the same inputs as the English reference, in the same
    order -- a missing input means a silently ignored option;
  * wires every declared input into `variables`, and declares every variable
    it wires;
  * carries the same version, and its own language in the name;
  * leaves no untranslated marker behind;
  * has Jinja that compiles -- an unbalanced `{%- if -%}` otherwise only
    surfaces when a user imports the blueprint and the automation silently
    stops firing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, TemplateSyntaxError

BLUEPRINTS = Path("blueprints/automation")
REFERENCE = "en"
LANGS = ["en", "fr", "de", "es", "it", "nl", "pl", "pt"]


class InputTag:
    """Stand-in for Home Assistant's `!input` tag."""

    def __init__(self, name: str) -> None:
        self.name = name


def _input(loader: yaml.SafeLoader, node: yaml.Node) -> InputTag:
    return InputTag(str(loader.construct_scalar(node)))  # type: ignore[arg-type]


yaml.SafeLoader.add_constructor("!input", _input)


def inputs_of(doc: dict) -> list[str]:
    """Every input name, flattened across sections, in declaration order."""
    names: list[str] = []
    for section in doc["blueprint"]["input"].values():
        names.extend(section["input"].keys())
    return names


def walk_templates(node: object, path: str = "") -> list[tuple[str, str]]:
    """Every string in the document that looks like a Jinja template."""
    found: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            found += walk_templates(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found += walk_templates(value, f"{path}[{index}]")
    elif isinstance(node, str) and ("{{" in node or "{%" in node):
        found.append((path.lstrip("."), node))
    return found


def main() -> int:
    errors: list[str] = []
    docs: dict[str, dict] = {}
    raw: dict[str, str] = {}

    for lang in LANGS:
        path = BLUEPRINTS / f"reef_maintenance_notify.{lang}.yaml"
        if not path.exists():
            errors.append(f"{lang}: missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        raw[lang] = text
        try:
            docs[lang] = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            errors.append(f"{lang}: does not parse -- {exc}")

    if REFERENCE not in docs:
        print("\n".join(errors) or "no reference file")
        return 1

    ref_inputs = inputs_of(docs[REFERENCE])
    ref_version = docs[REFERENCE]["blueprint"]["name"].rsplit("v", 1)[-1]

    for lang, doc in docs.items():
        bp = doc.get("blueprint", {})
        for key in ("name", "description", "domain", "source_url", "input"):
            if key not in bp:
                errors.append(f"{lang}: blueprint.{key} is missing")
        if bp.get("domain") != "automation":
            errors.append(f"{lang}: domain is not 'automation'")

        # Same options, same order, everywhere.
        got = inputs_of(doc)
        if got != ref_inputs:
            errors.append(
                f"{lang}: inputs differ from {REFERENCE}: {got} != {ref_inputs}"
            )

        # Every input must be wired into a variable, and every variable must
        # come from a declared input: a typo in either direction is silent.
        wired = {
            v.name for v in doc.get("variables", {}).values() if isinstance(v, InputTag)
        }
        for name in got:
            if name not in wired:
                errors.append(f"{lang}: input '{name}' is never used")
        for name in wired:
            if name not in got:
                errors.append(f"{lang}: variable reads undeclared input '{name}'")

        name = bp.get("name", "")
        if f"v{ref_version}" not in name:
            errors.append(f"{lang}: version differs from {REFERENCE} ({name})")
        if f"({lang})" not in name:
            errors.append(f"{lang}: name does not carry its language ({name})")

        # Jinja must compile. Only syntax is checked: the templates call
        # Home Assistant functions that do not exist here.
        # loopcontrols is what gives Jinja `{% break %}`. Home Assistant
        # enables it; plain Jinja2 does not, and without it a perfectly valid
        # template is reported as broken.
        env = Environment(extensions=["jinja2.ext.loopcontrols"])
        for path_str, tpl in walk_templates(doc):
            try:
                env.parse(tpl)
            except TemplateSyntaxError as exc:
                errors.append(f"{lang}: bad Jinja at {path_str} -- {exc}")

        # Placeholders the generator should have substituted.
        for marker in ("MSG_OVERDUE", "MSG_UNREACHABLE", "TITLE_PREFIX"):
            if marker in raw[lang]:
                errors.append(f"{lang}: unsubstituted marker {marker}")

        # A translated file that still holds the English message means a
        # missing entry in the generator's string table.
        if lang != REFERENCE:
            english = re.search(r"'Device unreachable'", raw[lang])
            if english:
                errors.append(f"{lang}: untranslated 'Device unreachable'")

    if errors:
        print("\n".join(f"  {e}" for e in errors))
        print(f"\n{len(errors)} problem(s) found.")
        return 1

    print(f"{len(docs)} blueprints, {len(ref_inputs)} inputs each, all consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
