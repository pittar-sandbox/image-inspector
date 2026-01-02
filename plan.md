# Test Update Plan

- [x] Inspect existing tests in `tests/test_app.py`
- [x] Create/Update tests for `index` route (GET /)
- [x] Create/Update tests for `inspect_image` route (POST /inspect)
    - [x] Test missing `image_url`
    - [x] Test successful inspection (mocked `skopeo`)
    - [x] Test `skopeo` failure (mocked error)
    - [x] Test `os_type` and `architecture` parameters
- [x] Run tests and ensure they pass
