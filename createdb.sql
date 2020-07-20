create table tasklist(
    id integer primary key,
    stage integer,
    marked boolean,
    created datetime,
    completed datetime,
    text text,
    description text,
    user_id integer
);

