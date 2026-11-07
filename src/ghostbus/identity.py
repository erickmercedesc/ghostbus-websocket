from collections.abc import Mapping
from urllib.parse import parse_qs

LICENSE_KEY_NAME = "X-License-Key"
_ENVIRON_HEADER = "HTTP_X_LICENSE_KEY"


def license_key_from(
    headers: Mapping[str, str],
    query: Mapping[str, str],
) -> str | None:
    raw = headers.get(LICENSE_KEY_NAME) or query.get(LICENSE_KEY_NAME)
    if raw is None:
        return None
    stripped = raw.strip()
    return stripped or None


def license_key_from_environ(environ: Mapping[str, str]) -> str | None:
    headers: dict[str, str] = {}
    header_value = environ.get(_ENVIRON_HEADER)
    if header_value is not None:
        headers[LICENSE_KEY_NAME] = header_value
    query_values = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)
    query = {name: values[0] for name, values in query_values.items() if values}
    return license_key_from(headers, query)
