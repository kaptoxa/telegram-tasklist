create table tasklist(
    id integer primary key,
    done boolean,
    marked boolean,
    idea boolean,
    created datetime,
    completed datetime,
    text text,
    description text,
    user_id integer
);

