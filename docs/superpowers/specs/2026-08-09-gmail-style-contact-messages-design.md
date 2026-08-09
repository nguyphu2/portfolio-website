# Gmail-style contact messages (design)

## Problem
`/admin/messages` currently marks every message as read the instant the
list page loads, so the unread/read distinction never has a chance to show.
The full message body is also printed inline in the list table.

## Goal
Make the admin messages list behave like an email inbox: unread messages
are visually distinct (bold/highlighted), and a message is only marked
read once the admin clicks into it to view the full body on its own page.

## Changes

### `app/routes/admin.py`
- `messages()` (list route): remove the loop that force-marks all messages
  read. Just query `Contact.query.order_by(Contact.created_at.desc())` and
  render.
- New `message_detail(id)` route at `/admin/messages/<int:id>`: fetch via
  `get_or_404`, set `is_read = True`, commit, render a detail template with
  the full name/email/message/timestamp.

### Templates
- `admin/messages.html`: each row links to `admin.message_detail`. Drop the
  full `message` column, replace with a short snippet (e.g. first ~60
  chars). Keep the existing `unread` row class / status column.
- New `admin/message_detail.html`: extends `base.html`; shows full name,
  email, message body, received timestamp, and a link back to the list.

### Styling (`app/static/css/style.css`)
- Keep `tr.unread` (bold + light background) for unread rows.
- Add a `.read` style that dims read rows (muted text color) so the
  contrast between read/unread is clear, satisfying the "greyed out once
  read" requirement.

## Out of scope
- No DB migration needed; `Contact.is_read` already exists.
- No pagination, search, delete, or reply functionality — list + detail
  view only.
