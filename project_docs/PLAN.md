# Mini Project 4 — Kansas Bill Tracker: Project Plan

## Overview

A Django web app that pulls live bill data from the Kansas Legislature KLISS REST API and lets users browse bills, comment on them, and upvote/downvote them. Admins can remove comments and attach written analysis summaries to bills via the Django admin panel.

---

## Dependencies

```
django
requests
django-crispy-forms
crispy-bootstrap5
```

SQLite is used as the database (Django default — no extra configuration needed).

---

## Project Structure

```
miniproject4/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                  # gitignored
├── ksbills/                    # Django project package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── bills/                      # main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   ├── services.py             # KLISS API logic isolated here
│   └── templates/
│       ├── base.html
│       ├── home.html
│       └── bills/
│           ├── bill_list.html
│           └── bill_detail.html
└── accounts/                   # auth app
    ├── views.py
    ├── urls.py
    └── templates/
        └── accounts/
            ├── register.html
            ├── login.html
            └── profile.html
```

---

## Data Models (SQLite)

### `Bill` — cached KLISS API data, refreshed on demand

| Field            | Type          | Notes                       |
|------------------|---------------|-----------------------------|
| `bill_number`    | CharField PK  | e.g. `"SB1"`                |
| `short_title`    | CharField     |                             |
| `long_title`     | TextField     |                             |
| `status`         | CharField     |                             |
| `sponsors`       | TextField     | comma-separated             |
| `effective_date` | TextField     | nullable                    |
| `last_fetched`   | DateTimeField | used for cache invalidation |

### `BillAnalysis` — admin-written summaries

| Field        | Type               |
|--------------|--------------------|
| `bill`       | FK → Bill          |
| `body`       | TextField          |
| `created_by` | FK → User          |
| `created_at` | DateTimeField auto |

### `Comment`

| Field        | Type               |
|--------------|--------------------|
| `bill`       | FK → Bill          |
| `author`     | FK → User          |
| `body`       | TextField          |
| `created_at` | DateTimeField auto |

### `Vote`

| Field           | Type         | Notes                            |
|-----------------|--------------|----------------------------------|
| `bill`          | FK → Bill    |                                  |
| `user`          | FK → User    |                                  |
| `value`         | IntegerField | `+1` (upvote) or `-1` (downvote) |
| unique_together | (bill, user) | one vote per user per bill       |

---

## Pages (6 total)

| URL                     | Page                                               | Form?        |
|-------------------------|----------------------------------------------------|--------------|
| `/`                     | Home — recent bills + site intro                   | —            |
| `/bills/`               | Bill list — all current session bills, search bar  | search (GET) |
| `/bills/<bill_number>/` | Bill detail — full info, analysis, comments, votes | comment form |
| `/accounts/register/`   | Register                                           | register form|
| `/accounts/login/`      | Login                                              | login form   |
| `/accounts/profile/`    | Profile — user's own comments                      | —            |

**Bootstrap modal:** Delete-comment confirmation modal on bill detail page — user clicks delete, modal confirms before submitting.

---

## Admin Panel

| Model           | Admin customization                                         |
|-----------------|-------------------------------------------------------------|
| `Bill`          | list display: bill_number, status; search by number/title   |
| `Comment`       | list display: author, bill, date; delete action; filter by bill |
| `BillAnalysis`  | inline on Bill admin for writing summaries per bill         |
| `Vote`          | read-only list showing vote tallies                         |

---

## KLISS API

Base URL: `https://www.kslegislature.gov/li/api/v10/rev-1/`

Key endpoints:
- `/bill_status/` — list all bills in current session
- `/bill_status/<bill_number>/` — full detail for a single bill

API requires a browser-like `User-Agent` header. All fetching is handled in `bills/services.py`.

Bill fields returned: `BILLNO`, `SHORTTITLE`, `LONGTITLE`, `STATUS`, `SPONSOR_NAMES`, `EFFECTIVEDATE`, `HISTORY`

---

## Commit Plan

| # | Message                                                      | Contents                                                   |
|---|--------------------------------------------------------------|------------------------------------------------------------|
| 1 | `init: scaffold Django project and bills app`                | `manage.py`, project package, app skeleton, settings, URLs |
| 2 | `models: add Bill, Comment, Vote, BillAnalysis + migrations` | all models + initial migration                             |
| 3 | `api: KLISS integration and bill list/detail views`          | `services.py`, bill views, templates                       |
| 4 | `auth: register, login, logout, and profile views`           | accounts app, auth templates                               |
| 5 | `interaction: comments and upvote/downvote system`           | comment form POST, vote POST, profile page                 |
| 6 | `admin: customize admin panel with inlines and list display` | `admin.py` with all models registered and styled           |
| 7 | `polish: Bootstrap modals, README, requirements.txt`         | delete modal, final template polish, docs                  |
