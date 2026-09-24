"""Checkable specifics in an answer, compared with what the tools returned in the same session.

An answer that names a URL, an e-mail address, a Swiss telephone number or a money amount that no tool output of
the session contains (and the user's question did not supply) states a specific the server did not serve. This is
the most common failure of grounded answers: the facts are right, and a document list, a fee or a plausible link is
added from memory. Dates are not compared, because deriving a deadline from a supplied date is expected; general
numbers are not compared, because they are too noisy.
"""

import json
import re
from urllib.parse import unquote

# A URL with a scheme, or a bare host name ending in a Swiss, generic or German top-level domain.
URL = re.compile(r"(?:https?://)?(?:www\.)?((?:[a-z0-9][a-z0-9-]*\.)+(?:ch|swiss|com|org|net|de|eu|info))\b(/[^\s)\]>\"'`*|,;]*)?",
                 re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
# Swiss numbers: 0 or +41/0041, area or mobile code, seven further digits, with the usual separators.
PHONE = re.compile(r"(?<![\d+])(?:\+41|0041|0)\s*(?:\(0\)\s*)?\d{2}(?:[\s./-]*\d){7}(?!\d)")
# "Fr." is left out: in opening hours it abbreviates Freitag ("Fr. 07:00-14:00").
AMOUNT = re.compile(r"(?:CHF|SFr\.?)\s*\d[\d'’ .,]*|\d[\d'’.,]*\s*(?:CHF|Franken|francs|Swiss francs)", re.I)


def normalize_url(host: str, path: str | None) -> str:
    path = unquote(path or "").split("#")[0].split("?")[0].rstrip("/.:")
    return host.lower().removeprefix("www.") + path.lower()


def normalize_phone(text: str) -> str:
    digits = re.sub(r"\D", "", text.replace("(0)", ""))
    if digits.startswith("0041"):
        digits = "0" + digits[4:]
    elif digits.startswith("41") and text.strip().startswith("+"):
        digits = "0" + digits[2:]
    return digits


def normalize_amount(text: str) -> str:
    number = re.sub(r"[^\d.,]", "", text)
    number = re.sub(r"[.,](?:\d{2}|-)?$", "", number)  # decimals or ".-"
    return re.sub(r"[.,]", "", number).lstrip("0") or "0"


def extract(text: str) -> dict[str, set[str]]:
    """Normalized URLs, e-mail addresses, telephone numbers and amounts found in a text."""
    emails = {m.lower() for m in EMAIL.findall(text)}
    # An e-mail domain is not a URL.
    without_emails = EMAIL.sub(" ", text)
    return {"urls": {normalize_url(m.group(1), m.group(2)) for m in URL.finditer(without_emails)},
            "emails": emails,
            "phones": {normalize_phone(m) for m in PHONE.findall(text)},
            "amounts": {normalize_amount(m) for m in AMOUNT.findall(text)}}


def output_text(output: str) -> str:
    """The string values of a JSON tool output, decoded; escapes such as \\t would otherwise glue onto a word."""
    try:
        data = json.loads(output)
    except ValueError:
        return output
    parts = []

    def walk(value):
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(data)
    return "\n".join(parts)


def merge(items) -> dict[str, set[str]]:
    merged = {"urls": set(), "emails": set(), "phones": set(), "amounts": set()}
    for item in items:
        for kind, values in item.items():
            merged[kind] |= set(values)
    return merged


def unserved(answer: str, served: dict[str, set[str]], supplied: str = "") -> dict[str, list[str]]:
    """Specifics of the answer that neither the served outputs nor the user's own text contain.

    A bare host (wallisellen.ch) counts as served when any served URL is on that host; a path must match exactly.
    """
    found = extract(answer)
    allowed = merge([served, extract(supplied)])
    hosts = {url.split("/", 1)[0] for url in allowed["urls"]}
    result = {}
    for kind, values in found.items():
        missing = []
        for value in sorted(values):
            if value in allowed[kind]:
                continue
            if kind == "urls" and "/" not in value and value in hosts:
                continue
            missing.append(value)
        result[kind] = missing
    return result
