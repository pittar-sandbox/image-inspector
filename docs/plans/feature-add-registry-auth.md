# Feature: Add Registry Authentication Support

## Goal
Add UI elements for a user to include their image registry username and password in order to allow skopeo to inspect images in private repositories. Update the backend python app to handle these credentials securely.

## Todo List
- [ ] Create a new git branch `feature/add-registry-auth`
- [ ] Update `templates/index.html` to include input fields for Username and Password
- [ ] Update `app.py` to:
    - [ ] Retrieve `username` and `password` from the request
    - [ ] Add `--creds username:password` to the skopeo command if credentials are provided
    - [ ] Ensure the password is masked or omitted in application logs
- [ ] Update `tests/test_app.py` to verify that credentials are correctly passed to the skopeo command
- [ ] Run tests to ensure no regressions and new features work as expected
