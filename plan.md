# UI Improvements Plan

## Task: Improve UI to display specific image details

The goal is to update the UI to parse and display specific details from the image inspection data, rather than just dumping the raw JSON.

### Required Fields to Display:
*   Image name
*   Total image size (sum of `LayersData` sizes)
*   OS type
*   Architecture
*   Number of layers

### Steps:

1.  **Analyze Existing Code**:
    *   Review `app.py` to ensure backend sends necessary data (it seems to send raw skopeo output, which contains the needed info).
    *   Review `templates/index.html` to see current rendering logic.

2.  **Update `plan.md`**:
    *   Document the task and steps.

3.  **Modify Frontend (`templates/index.html`)**:
    *   Update the JavaScript to parse the JSON response.
    *   Calculate "Total image size" by summing `Size` field in `LayersData`.
    *   Create HTML elements to display the specific fields.
    *   Keep the raw JSON display but maybe hide it behind a "Show Raw Data" toggle or just below the summary.

4.  **Test**:
    *   Verify the UI correctly displays the information.
    *   Since I cannot browse the UI, I will rely on reading the code and potentially adding a test case that verifies the HTML structure or just unit testing the calculation logic if I were to move it to backend.
    *   Wait, the instructions say "The UI needs work". I should probably do the calculation in the frontend as requested ("The UI should have specific display elements"). However, logic is often better in backend. But for this task, I will stick to modifying the UI (template) as implied. Actually, calculating size in backend might be cleaner. Let's see. The user says "The UI needs work", so I will focus on `index.html`.

5.  **Verify Tests**:
    *   Run existing tests to ensure no regressions.
    *   Add a test case if possible to verify the endpoint still works.

### TODOs

- [ ] Create `plan.md` (Current Step)
- [ ] Create/Update unit tests to verify backend response structure (if needed)
- [ ] Modify `templates/index.html` to implement the new UI requirements
- [ ] Verify changes with tests
