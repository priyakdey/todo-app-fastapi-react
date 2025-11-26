-- profile table contains the primary information about the users
create table profile
(
    id          serial,
    username    varchar(20),
    password    varchar(20),
    name        varchar(100),
    created_on  bigint,
    modified_on bigint,
    primary key(id)
);


create table todo
(
    id serial,
    profile_id int,
    title varchar(50),
    description text,
    is_completed boolean,
    created_on bigint,
    modified_on bigint,
    primary key(id),
    constraint fk_profile_id
        foreign key (profile_id)
        references profile (id)
        on delete cascade
);


