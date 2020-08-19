create table tasklist(
    id integer primary key,
    stage integer,
    created datetime,
    changed datetime,
    text text,
    tags text,
    user_id integer,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

create table users(
    id integer primary key,
    name varchar(255),
    days integer
);


