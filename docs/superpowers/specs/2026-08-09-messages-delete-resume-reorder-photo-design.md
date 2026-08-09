# Message delete, resume drag-and-drop reorder, resume photo upload (design)

## 1. Delete messages
- New `POST /admin/messages/<int:id>/delete` route in `app/routes/admin.py`,
  mirroring the existing `delete_project` pattern: `get_or_404`, delete,
  commit, redirect to `admin.messages`.
- Delete button/form added to `admin/message_detail.html`.

## 2. Drag-and-drop reorder for resume sections
- `admin/resume.html`: drop the numeric "Order" column, add a drag handle
  per row. Rows become draggable via native HTML5 drag-and-drop
  (`draggable`, `dragstart`/`dragover`/`drop` handlers) - no external JS
  library.
- On drop, client JS POSTs the full ordered list of section ids as JSON to
  a new `POST /admin/resume/reorder` endpoint.
- That route walks the id list and sets `order_index = position` for each
  section, then commits.
- `resume_form.html`: remove the manual `order_index` input. New sections
  get `order_index` set to `max(existing) + 1` (appended at the end) in
  `new_resume_section`.

## 3. Photo upload for resume sections
- No migration framework exists in this project (tables were hand-created,
  no Flask-Migrate/Alembic). Add the column directly:
  `ALTER TABLE resume_section ADD COLUMN photo_filename VARCHAR(300);`
- `app/models/resume.py`: add `photo_filename = db.Column(db.String(300), nullable=True)`.
- `resume_form.html`: add `<input type="file" name="photo">` (form needs
  `enctype="multipart/form-data"`).
- `new_resume_section` / `edit_resume_section`: if `request.files.get('photo')`
  has content, save it via `werkzeug.utils.secure_filename` into
  `app/static/img/resume/`, store the resulting filename on the row.
  Editing without picking a new file leaves the existing photo untouched.
- Display the photo as a thumbnail in `admin/resume.html` and next to the
  matching section on the public `resume.html` page.

## Out of scope
- No image resizing/validation beyond basic file extension allowlist.
- No reordering across section types (drag-and-drop reorders the full flat
  list as currently rendered, same ordering scope as today's order_index).
