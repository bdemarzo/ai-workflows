# Spec - saved-views-full-workflow

## User Contract
- Users can save the current filter state as a named saved view.
- Users can load, rename, and delete their own saved views.
- Loading a saved view reapplies the stored filters to the dashboard.

## Important Boundaries
- Saved views are per-user in v1.
- The feature does not include team sharing in v1.
- Invalid or deleted filters must surface a clear user-visible fallback state.
