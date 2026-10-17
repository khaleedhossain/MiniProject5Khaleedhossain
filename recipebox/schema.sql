DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS ingredient;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Each recipe belongs to the user who created it.
CREATE TABLE recipe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  instructions TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

-- Each ingredient line belongs to one recipe; position keeps the list order.
CREATE TABLE ingredient (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES recipe (id)
);
