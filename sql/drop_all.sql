drop materialized view if exists search_index cascade;

drop table if exists attachment cascade;

drop table if exists contact_person cascade;

drop table if exists guide cascade;

drop table if exists employee cascade;

drop table if exists project_registration cascade;

drop table if exists "like" cascade;

drop table if exists project_click cascade;

drop table if exists query cascade;

drop table if exists session cascade;

drop table if exists student cascade;

drop table if exists project_has_type cascade;

drop table if exists type cascade;

drop table if exists link cascade;

drop table if exists project_has_year cascade;

drop table if exists project_has_tag cascade;

drop table if exists project cascade;

drop table if exists research_group cascade;

drop table if exists document cascade;

drop table if exists tag;

drop index if exists idx_fts_search;

drop type if exists employeetitle cascade;

drop type if exists guidancetype cascade;

drop type if exists registrationstatus cascade;

