# ts-python-api-sln

Implements:
- API contract tests for `GET /api/shipments/{shipment_id}` (offline, based on provided sample contract)
- Data quality validation checks for ingestion payloads (offline, based on provided sample events)
- Postman smoke collection (empty) for quick manual sanity checks (local)

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest