# Recipe Box — Mini Project 5

**INF601 – Advanced Programming in Python**
Khaleed Hossain

A small Flask web app for keeping a personal collection of recipes. Users
register and log in, then add their own recipes — a title, an ingredient
list, and instructions — and can edit or delete only the recipes they
authored. Anyone, logged in or not, can browse and read recipes.

## Project layout

Modeled directly on the structure from the official Flask tutorial (an
application factory plus blueprints), rather than one flat script:

```
MiniProject5Khaleedhossain/
├── recipebox/
│   ├── __init__.py       # create_app() — the application factory
│   ├── db.py             # SQLite connection handling + `flask init-db`
│   ├── schema.sql        # table definitions
│   ├── auth.py           # register / login / logout blueprint
│   ├── recipes.py        # recipe list / detail / create / update / delete blueprint
│   ├── templates/
│   │   ├── base.html             # shared layout, navbar, Bootstrap
│   │   ├── auth/
│   │   │   ├── register.html
│   │   │   └── login.html
│   │   └── recipes/
│   │       ├── index.html        # all recipes, card grid
│   │       ├── detail.html       # one recipe + its ingredients + delete modal
│   │       ├── create.html       # new recipe form (GET shows it, POST saves it)
│   │       └── update.html       # edit form, same GET/POST pattern
│   └── static/
│       └── style.css
├── requirements.txt
└── .gitignore
```

## Database

SQLite, three tables, two foreign-key relationships (`schema.sql`):

| Table | Columns | Linked by |
|---|---|---|
| `user` | id, username, password (hashed) | — |
| `recipe` | id, author_id, title, instructions, created | `author_id` → `user.id` |
| `ingredient` | id, recipe_id, position, description | `recipe_id` → `recipe.id` |

A recipe's ingredients are entered as one per line in a textarea and stored
as separate `ingredient` rows (ordered by `position`), rather than as one
blob of text — so each ingredient is its own row linked back to its recipe.

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Initialize the database (creates `instance/recipebox.sqlite` from
`schema.sql` — destructive if the file already exists, so only run this
once at the start, or again if you want to wipe all data):

```bash
export FLASK_APP=recipebox       # Windows (PowerShell): $env:FLASK_APP="recipebox"
flask init-db
```

Run the development server:

```bash
flask run --debug
```

Then open <http://127.0.0.1:5000>. Register an account, log in, and add a
recipe. Logged-out visitors can still browse and read every recipe; only
the recipe's own author can edit or delete it (enforced server-side, not
just hidden in the UI — a direct POST to someone else's recipe returns
`403`).

## Pages

| Route | Page | Notes |
|---|---|---|
| `/` | Recipe list | Public. Card grid of every recipe. |
| `/<id>` | Recipe detail | Public. Ingredients + instructions; delete button (owner only) opens a **Bootstrap modal** to confirm before the destructive POST fires. |
| `/create` | New recipe | Login required. Form, `GET` renders it / `POST` validates and saves it. |
| `/<id>/update` | Edit recipe | Login + ownership required. Same GET/POST form pattern, pre-filled. |
| `/auth/register` | Register | Form, `GET`/`POST`. |
| `/auth/login` | Log in | Form, `GET`/`POST`. |

Bootstrap 5 (via CDN) styles the navbar, forms, cards, alerts, and the
delete-confirmation modal on the detail page.

## AI Usage

This project was built with Claude Code. Breakdown of what the AI did
versus what I directed and reviewed:

**Done by Claude Code:**
- Scaffolded the application-factory/blueprint structure (`recipebox/`,
  `templates/`, `static/`) modeled on the official Flask tutorial, adapted
  from a blog (title/body) to a recipe box (title/ingredients/instructions)
  at my direction.
- Wrote `db.py`, `schema.sql` (including the `ingredient` table and its
  foreign key to `recipe`, beyond the minimum two linked tables), `auth.py`,
  `recipes.py`, and all six page templates.
- Added Bootstrap 5 via CDN to `base.html` and built the delete-confirmation
  modal on the recipe detail page.
- Installed dependencies, initialized the database, started the dev server,
  and exercised the full app with `curl`: register, login, create a recipe
  (confirming the ingredient rows were each inserted and linked by
  `recipe_id`), view it on the index and detail pages, update it, confirm a
  second user gets `403` trying to edit the first user's recipe, confirm
  anonymous users can read but not create, and delete it (confirming a 404
  afterward).

**Done by me:**
- Chose the recipe-box concept and the data model (what a recipe needs
  beyond title/body: a real ingredients list as its own linked table).
- Reviewed the authorization logic (ownership check on update/delete) and
  the template inheritance structure.
- Ran and clicked through the app myself to confirm the register → login →
  create → edit → delete flow and the Bootstrap modal behave as described
  above.

## Requirements coverage

- Application factory + blueprints, modeled on the tutorial.
- 6 page templates (register, login, index, detail, create, update), all
  extending a shared `base.html`.
- `/create` and `/<id>/update`: forms with proper `GET` (render) and `POST`
  (validate + save) routes.
- SQLite database, three tables, two foreign-key relationships.
- Bootstrap 5, including a modal (delete confirmation).
- Register/login system with hashed passwords and session-based auth.
