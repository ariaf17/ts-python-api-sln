from tests.utils import load_json, parse_iso8601

def test_validate_get_shipment_response():
    data = load_json("samples/api/get_shipment_response.json")
    
    required = ["shipment_id", "status", "origin", "destination", "carrier", "container_id", "events", "eta", "last_updated"]
    
    for field in required:
        assert field in data, f"Missing required field: {field}"

    assert isinstance(data["shipment_id"], str) and data["shipment_id"] != ""
    assert isinstance(data["status"], str) and data["status"] != ""   
    assert isinstance(data["origin"], dict)
    assert "port" in data["origin"] and "country" in data["origin"]
    assert isinstance(data["carrier"], str), "carrier should be a string" and data["carrier"] != ""
    assert isinstance(data["container_id"], str), "container_id should be a string" and data["container_id"] != ""
    assert isinstance(data["events"], list), "events should be a list" and all(isinstance(event, dict) for event in data["events"]) > 0
    assert isinstance(data["eta"], str), "eta should be a string" and parse_iso8601(data["eta"])
    assert isinstance(data["last_updated"], str), "last_updated should be a string" and parse_iso8601(data["last_updated"])

    # Contract: checks per sample API contract; origin and destination must have port and country fields
    assert "port" in data["origin"] and "country" in data["origin"]
    assert "port" in data["destination"] and "country" in data["destination"]

    assert isinstance(data["events"], list) and len(data["events"]) > 0

    # Contract: timestamps parse as ISO8601
    parse_iso8601(data["eta"])
    parse_iso8601(data["last_updated"])

    # Each event must have these fields per sample API contract
    for e in data["events"]:
        for ef in ["timestamp", "type", "source"]:
            assert ef in e, f"Missing event field: {ef}"
        parse_iso8601(e["timestamp"])

# 'last_updated' should represent the freshest known event time
# This test checks that 'last_updated' is equal to the maximum timestamp among the events, ensuring consistency in the data
def test_last_updated_equals_latest_event_timestamp():
    data = load_json("samples/api/get_shipment_response.json")

    last_updated = parse_iso8601(data["last_updated"])
    event_timestamp = [parse_iso8601(e["timestamp"]) for e in data["events"]]

    assert last_updated == max(event_timestamp)
    