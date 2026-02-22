from tests.utils import load_json, parse_iso8601

# Validation logic for ingestion events, based on the sample payloads and expected fields per source. 
# This is a simplified example; real implementation would likely be more complex and involve schema validation libraries, more detailed error reporting, and integration with the actual ingestion pipeline.
# The tests below use this validation logic to check that the sample ingestion payloads are correctly classified based on their content.
# This part of the task was very challenging for me and I referenced a lot of open-source material/AI tips to get this working.
# My main goal was to demonstrate a simple validation approach that could be expanded upon in a real implementation.
def validate_event(payload: dict) -> tuple[str, list[str]]:
    errors: list[str] = []

    source = payload.get("source")
    if not source:
        return "Reject", ["Missing Source"]

    # Required fields per source based on the sample igestion payloads
    if source == "carrier_cdc":
        required = ["shipment_id", "status", "timestamp", "port"]
    elif source == "edge_sensor":
        required = ["device_id", "container_id", "timestamp", "lat", "lon"]
    elif source == "email_parser":
        required = ["shipment_ref", "status", "timestamp"]
    else:
        return "Reject", [f"Unknown Source: {source}"]

    # Required field presence
    for field in required:
        if payload.get(field) in (None, ""):
            errors.append(f"Missing/Invalid Field: {field}")

    # Timestamp validation if present and non-empty
    timestamp = payload.get("timestamp")
    if timestamp not in (None, ""):
        try:
            parse_iso8601(timestamp)
        except Exception:
            errors.append("Invalid timestamp format (expected ISO8601)")

    action = "Accept" if not errors else "Warning"
    return action, errors


def test_carrier_cdc_event_is_accepted():
    payload = load_json("samples/ingestion/carrier_cdc_event.json")
    action, errors = validate_event(payload)
    assert action == "Accept"
    assert errors == []


def test_edge_sensor_event_is_accepted():
    payload = load_json("samples/ingestion/edge_sensor_event.json")
    action, errors = validate_event(payload)
    assert action == "Accept"
    assert errors == []


def test_email_parser_null_timestamp_is_warning():
    payload = load_json("samples/ingestion/email_parser_event.json")
    action, errors = validate_event(payload)
    assert action == "Warning"
    assert any("timestamp" in e for e in errors)