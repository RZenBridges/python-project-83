DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls(
    id serial PRIMARY KEY,
    name varchar(255) UNIQUE,
    created_at timestamp
);


CREATE TABLE url_checks(
    id serial PRIMARY KEY,
    url_id int REFERENCES urls (id) ON DELETE CASCADE,
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at timestamp
);
