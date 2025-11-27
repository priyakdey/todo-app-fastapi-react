-- profile table contains the primary information about the users
create table profile
(
    id          serial,
    username    varchar(20)  not null unique,
    password    varchar(20)  not null,
    name        varchar(100) not null,
    created_on  bigint       not null,
    modified_on bigint       not null,
    primary key(id)
);


create table todo
(
    id           serial,
    profile_id   int,
    title        varchar(50) not null,
    description  text,
    is_completed boolean not null,
    created_on   bigint not null,
    modified_on  bigint not null,
    primary key(id),
    constraint fk_profile_id
        foreign key (profile_id)
        references profile (id)
        on delete cascade
);


