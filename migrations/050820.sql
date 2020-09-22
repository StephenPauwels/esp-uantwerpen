alter table project_registration
add column type varchar(255) references Type(type_name) ON update cascade on delete cascade ;
