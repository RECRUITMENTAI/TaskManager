# Feature Request

## Feature: Task Counter Display
**Priority:** Medium  
**Requested By:** Human  
**Date:** 2025-08-01

## Description
Add a simple task counter that shows the total number of tasks on the homepage. This will provide users with a quick overview of their task load.

## Requirements
- [ ] Display "Total Tasks: X" on the main homepage
- [ ] Counter should update dynamically when tasks are added/removed
- [ ] Place counter in a visible location (near the header or add task form)
- [ ] Use simple styling that matches existing design
- [ ] No complex JavaScript needed - server-side rendering is fine

## Implementation Notes
- Keep it simple for demo purposes
- Focus on visible, functional changes
- Ensure it works with existing Flask app structure
- Can reuse existing `get_all_tasks()` function
- Add counter to HTML template

## Acceptance Criteria
- [ ] Counter displays correct total number of tasks
- [ ] Counter updates when tasks are added
- [ ] Counter updates when tasks are deleted
- [ ] Tests pass
- [ ] No breaking changes to existing functionality
- [ ] Ready for deployment

---
*This file will be read by python-api-builder agent for implementation*