# INF601 - Advanced Programming in Python
# Khaleed Hossain
# Mini Project 5

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from recipebox.auth import login_required
from recipebox.db import get_db

bp = Blueprint("recipes", __name__)


def split_ingredients(raw):
    """Turn the textarea's newline-separated text into a clean list of lines."""
    return [line.strip() for line in raw.splitlines() if line.strip()]


@bp.route("/")
def index():
    db = get_db()
    recipes = db.execute(
        "SELECT r.id, title, created, author_id, username"
        " FROM recipe r JOIN user u ON r.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("recipes/index.html", recipes=recipes)


def get_recipe(id, check_author=True):
    recipe = (
        get_db()
        .execute(
            "SELECT r.id, title, instructions, created, author_id, username"
            " FROM recipe r JOIN user u ON r.author_id = u.id"
            " WHERE r.id = ?",
            (id,),
        )
        .fetchone()
    )

    if recipe is None:
        abort(404, f"Recipe id {id} doesn't exist.")

    if check_author and recipe["author_id"] != g.user["id"]:
        abort(403)

    return recipe


def get_ingredients(recipe_id):
    return (
        get_db()
        .execute(
            "SELECT id, description FROM ingredient"
            " WHERE recipe_id = ? ORDER BY position",
            (recipe_id,),
        )
        .fetchall()
    )


@bp.route("/<int:id>")
def detail(id):
    recipe = get_recipe(id, check_author=False)
    ingredients = get_ingredients(id)
    return render_template(
        "recipes/detail.html", recipe=recipe, ingredients=ingredients
    )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        instructions = request.form["instructions"]
        ingredients = split_ingredients(request.form["ingredients"])
        error = None

        if not title:
            error = "Title is required."
        elif not ingredients:
            error = "At least one ingredient is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.execute(
                "INSERT INTO recipe (title, instructions, author_id)"
                " VALUES (?, ?, ?)",
                (title, instructions, g.user["id"]),
            )
            recipe_id = cur.lastrowid
            db.executemany(
                "INSERT INTO ingredient (recipe_id, position, description)"
                " VALUES (?, ?, ?)",
                [(recipe_id, i, text) for i, text in enumerate(ingredients)],
            )
            db.commit()
            return redirect(url_for("recipes.detail", id=recipe_id))

    return render_template("recipes/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    recipe = get_recipe(id)
    ingredients = get_ingredients(id)

    if request.method == "POST":
        title = request.form["title"]
        instructions = request.form["instructions"]
        new_ingredients = split_ingredients(request.form["ingredients"])
        error = None

        if not title:
            error = "Title is required."
        elif not new_ingredients:
            error = "At least one ingredient is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE recipe SET title = ?, instructions = ? WHERE id = ?",
                (title, instructions, id),
            )
            db.execute("DELETE FROM ingredient WHERE recipe_id = ?", (id,))
            db.executemany(
                "INSERT INTO ingredient (recipe_id, position, description)"
                " VALUES (?, ?, ?)",
                [(id, i, text) for i, text in enumerate(new_ingredients)],
            )
            db.commit()
            return redirect(url_for("recipes.detail", id=id))

    return render_template(
        "recipes/update.html", recipe=recipe, ingredients=ingredients
    )


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_recipe(id)
    db = get_db()
    db.execute("DELETE FROM ingredient WHERE recipe_id = ?", (id,))
    db.execute("DELETE FROM recipe WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("recipes.index"))
