DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE,
    created_at DATE
);


CREATE TABLE url_checks(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id int REFERENCES urls (id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at DATE
);
