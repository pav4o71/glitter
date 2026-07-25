#!/usr/bin/env python3
"""Dependency-free structural audit for the Glitter Professional website."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = (ROOT / "index.html", ROOT / "services.html")
EXTERNAL_SCHEMES = {"http", "https", "tel", "mailto", "sms", "data", "javascript"}
REQUIRED_CONTENT = {
    "display phone": "0917 830 1584",
    "telephone link": "tel:09178301584",
    "SMS link": "sms:+639178301584",
    "email": "glitterprofessional@gmail.com",
    "Messenger link": "https://m.me/GlitterProfessional",
    "Instagram DM link": "https://ig.me/m/glitterprofessional",
    "street address": "994 Quirino Avenue",
    "opening hours": "10:00 AM–9:00 PM",
}
FORBIDDEN_TEXT = {
    "example.com": "production metadata must not use a placeholder domain",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[tuple[str, int]] = []
        self.references: list[tuple[str, str, int]] = []
        self.images_without_alt: list[int] = []
        self.json_ld: list[tuple[str, int]] = []
        self.blank_links_without_rel: list[tuple[str, int]] = []
        self.h1_count = 0
        self.lang: str | None = None
        self.title_depth = 0
        self.title_text: list[str] = []
        self._json_line: int | None = None
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        line, _ = self.getpos()

        if tag == "html":
            self.lang = attributes.get("lang")
        if tag == "title":
            self.title_depth += 1
        if tag == "h1":
            self.h1_count += 1

        element_id = attributes.get("id")
        if element_id:
            self.ids.append((element_id, line))

        if tag == "img" and "alt" not in attributes:
            self.images_without_alt.append(line)

        if tag in {"a", "link"}:
            href = attributes.get("href")
            if href:
                self.references.append(("href", href, line))
            if tag == "a" and attributes.get("target") == "_blank":
                rel = set((attributes.get("rel") or "").split())
                if not {"noopener", "noreferrer"}.issubset(rel):
                    self.blank_links_without_rel.append((href or "(missing href)", line))

        if tag in {"img", "script"}:
            src = attributes.get("src")
            if src:
                self.references.append(("src", src, line))

        if tag in {"img", "source"}:
            srcset = attributes.get("srcset")
            if srcset:
                for candidate in srcset.split(","):
                    candidate_url = candidate.strip().split(maxsplit=1)[0]
                    if candidate_url:
                        self.references.append(("srcset", candidate_url, line))

        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_line = line
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        if tag == "script" and self._json_line is not None:
            self.json_ld.append(("".join(self._json_parts), self._json_line))
            self._json_line = None
            self._json_parts = []

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)
        if self._json_line is not None:
            self._json_parts.append(data)


def parse_page(path: Path) -> tuple[str, PageParser]:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return text, parser


def target_ids(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    resolved = path.resolve()
    if resolved not in cache:
        if not resolved.exists() or resolved.suffix.lower() != ".html":
            cache[resolved] = set()
        else:
            _, parser = parse_page(resolved)
            cache[resolved] = {element_id for element_id, _ in parser.ids}
    return cache[resolved]


def audit() -> list[str]:
    errors: list[str] = []
    id_cache: dict[Path, set[str]] = {}

    for page in HTML_FILES:
        if not page.exists():
            errors.append(f"{page.name}: file is missing")
            continue

        text, parser = parse_page(page)
        id_cache[page.resolve()] = {element_id for element_id, _ in parser.ids}

        id_counts = Counter(element_id for element_id, _ in parser.ids)
        for element_id, count in sorted(id_counts.items()):
            if count > 1:
                errors.append(f"{page.name}: duplicate id #{element_id} ({count} occurrences)")

        if parser.lang != "en":
            errors.append(f"{page.name}: expected html lang=\"en\"")
        if not "".join(parser.title_text).strip():
            errors.append(f"{page.name}: document title is missing")
        if parser.h1_count != 1:
            errors.append(f"{page.name}: expected exactly one h1, found {parser.h1_count}")

        for line in parser.images_without_alt:
            errors.append(f"{page.name}:{line}: image is missing an alt attribute")

        for href, line in parser.blank_links_without_rel:
            errors.append(
                f"{page.name}:{line}: target=_blank link lacks noopener/noreferrer: {href}"
            )

        for payload, line in parser.json_ld:
            try:
                json.loads(payload)
            except json.JSONDecodeError as error:
                errors.append(
                    f"{page.name}:{line}: invalid JSON-LD: {error.msg} "
                    f"(line {error.lineno}, column {error.colno})"
                )

        for label, required in REQUIRED_CONTENT.items():
            if required not in text:
                errors.append(f"{page.name}: missing required {label}: {required}")

        lowered = text.lower()
        for forbidden, reason in FORBIDDEN_TEXT.items():
            if forbidden in lowered:
                errors.append(f"{page.name}: found {forbidden!r}; {reason}")

        for attribute, reference, line in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme.lower() in EXTERNAL_SCHEMES or reference.startswith("//"):
                continue

            reference_path = unquote(parsed.path)
            target_path = (page.parent / reference_path).resolve() if reference_path else page
            if reference_path and not target_path.exists():
                errors.append(
                    f"{page.name}:{line}: broken local {attribute} reference: {reference}"
                )
                continue

            if parsed.fragment:
                fragment = unquote(parsed.fragment)
                if fragment not in target_ids(target_path, id_cache):
                    errors.append(
                        f"{page.name}:{line}: missing fragment #{fragment} in "
                        f"{target_path.name}"
                    )

    return errors


def main() -> int:
    errors = audit()
    if errors:
        print(f"Site audit failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Site audit passed: 2 pages, local references, fragments, JSON-LD, "
        "image alternatives, contact details, and launch placeholders are valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
