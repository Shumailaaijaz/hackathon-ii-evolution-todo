# Testing Checklist

## Backend Unit Tests

- [ ] User model tests (validation, constraints)
- [ ] Task model tests (validation, relationships)
- [ ] JWT verification tests (valid, invalid, expired)
- [ ] Security utilities tests
- [ ] Pydantic schema validation tests

## Backend Integration Tests

- [ ] GET /api/{user_id}/tasks (success, filters, sorting)
- [ ] POST /api/{user_id}/tasks (success, validation errors)
- [ ] GET /api/{user_id}/tasks/{task_id} (success, 404, 403)
- [ ] PUT /api/{user_id}/tasks/{task_id} (success, validation)
- [ ] DELETE /api/{user_id}/tasks/{task_id} (success, 404, 403)
- [ ] PATCH /api/{user_id}/tasks/{task_id}/toggle (success)

## Authentication Tests

- [ ] Valid JWT accepted
- [ ] Invalid JWT rejected (401)
- [ ] Expired JWT rejected (401)
- [ ] Missing JWT rejected (401)
- [ ] User isolation enforced (403 for other user's tasks)
- [ ] Token refresh works

## Frontend Component Tests

- [ ] TaskCard renders correctly
- [ ] TaskCard checkbox toggles completion
- [ ] TaskCard edit button opens modal
- [ ] TaskCard delete button works
- [ ] TaskList displays tasks
- [ ] TaskList shows empty state
- [ ] CreateTaskForm validates input
- [ ] CreateTaskForm submits correctly
- [ ] TaskFilters update URL params

## End-to-End Tests

- [ ] User can sign up
- [ ] User can sign in
- [ ] User can create task
- [ ] User can edit task
- [ ] User can toggle completion
- [ ] User can delete task
- [ ] User can filter tasks
- [ ] User can sort tasks
- [ ] User can sign out

## Test Coverage

- [ ] Backend test coverage ≥90%
- [ ] Frontend test coverage ≥80%
- [ ] All critical paths covered
- [ ] Edge cases tested
- [ ] Error scenarios tested
