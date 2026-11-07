from ghostbus.identity import LICENSE_KEY_NAME, license_key_from, license_key_from_environ


def test_header_wins_over_query() -> None:
    key = license_key_from(
        headers={LICENSE_KEY_NAME: "from-header"},
        query={LICENSE_KEY_NAME: "from-query"},
    )
    assert key == "from-header"


def test_query_is_used_when_header_is_missing() -> None:
    key = license_key_from(headers={}, query={LICENSE_KEY_NAME: "from-query"})
    assert key == "from-query"


def test_blank_values_are_not_a_license() -> None:
    assert license_key_from(headers={LICENSE_KEY_NAME: "  "}, query={}) is None
    assert license_key_from(headers={}, query={}) is None


def test_environ_reads_header_then_query() -> None:
    from_header = license_key_from_environ(
        {
            "HTTP_X_LICENSE_KEY": "env-header",
            "QUERY_STRING": f"{LICENSE_KEY_NAME}=env-query",
        }
    )
    from_query = license_key_from_environ(
        {"QUERY_STRING": f"{LICENSE_KEY_NAME}=env-query"}
    )
    assert from_header == "env-header"
    assert from_query == "env-query"
