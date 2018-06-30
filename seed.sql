-- Seed script used to build up required tables, functions, triggers, and views.

DROP DATABASE IF EXISTS bubble_tea;

CREATE DATABASE bubble_tea;

\c bubble_tea;

DROP TABLE IF EXISTS bubble_tea;

CREATE TABLE IF NOT EXISTS bubble_tea (
    id varchar(32) primary key,
    alias varchar(255),
    name varchar(128),
    country varchar(128),
    address1 varchar(128),
    address2 varchar(128) default null,
    address3 varchar(128) default null,
    city varchar(128),
    state varchar(128) default null,
    zip_code varchar(128) default null,
    phone varchar(32) default null,
    latitude decimal(10, 6),
    longitude decimal(10, 6),
    rating decimal(2, 1),
    review_count int,
    url text,
    insert_dt timestamp default current_timestamp,
    update_dt timestamp default current_timestamp
);

CREATE INDEX idx_name ON bubble_tea (name);
CREATE INDEX idx_zip_code ON bubble_tea (zip_code);

CREATE OR REPLACE FUNCTION update_update_dt_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.update_dt = now();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_bubble_tea_update_dt BEFORE UPDATE
    ON bubble_tea FOR EACH ROW EXECUTE PROCEDURE
    update_update_dt_column();

-- https://www.unitedstateszipcodes.org/zip-code-database/
DROP TABLE IF EXISTS zip_code;

CREATE TABLE zip_code(
    id SERIAL,
    zip varchar(10),
    type varchar(255),
    decomissioned varchar(20),
    primary_city varchar(255),
    acceptable_cities text,
    unacceptable_cities text,
    state varchar(255),
    county varchar(255),
    timezone varchar(255),
    area_code varchar(255),
    world_region varchar(255),
    country varchar(255),
    latitude varchar(255),
    longitude varchar(255),
    irs_estimated_population_2015 varchar(255),
    insert_dt timestamp default current_timestamp,
    update_dt timestamp default current_timestamp
);

CREATE TRIGGER update_zip_code_update_dt BEFORE UPDATE
    ON zip_code FOR EACH ROW EXECUTE PROCEDURE
    update_update_dt_column();

\copy zip_code (zip, type, decomissioned, primary_city, acceptable_cities, unacceptable_cities, state, county, timezone, area_code, world_region, country, latitude, longitude, irs_estimated_population_2015) FROM './csvs/zip_code_database.csv' WITH delimiter ',' CSV HEADER;

-- https://www2.census.gov/geo/docs/reference/codes/files/st06_ca_cou.txt
DROP TABLE IF EXISTS county_to_fips_mapping;

CREATE TABLE county_to_fips_mapping (
    state varchar(2),
    state_fips varchar(2),
    county_fips varchar(3),
    county varchar(128)
);

\copy county_to_fips_mapping FROM './csvs/county_to_fips.csv' WITH delimiter ',' CSV;

DROP TABLE IF EXISTS hours;

CREATE TABLE hours (
    id SERIAL,
    bubble_tea_id varchar(32),
    day int,
    start varchar(4),
    "end" varchar(4),
    is_overnight bool,
    insert_dt timestamp default current_timestamp,
    update_dt timestamp default current_timestamp
);

CREATE UNIQUE INDEX idx_bubble_tea_id_day ON hours (bubble_tea_id, day);

CREATE TRIGGER update_hours_update_dt BEFORE UPDATE
    ON hours FOR EACH ROW EXECUTE PROCEDURE
    update_update_dt_column();

CREATE OR REPLACE VIEW bubble_tea_w_fips AS
SELECT
    bubble_tea.id,
    bubble_tea.name,
    bubble_tea.country,
    bubble_tea.address1,
    bubble_tea.address2,
    bubble_tea.address3,
    bubble_tea.city,
    bubble_tea.state,
    bubble_tea.zip_code,
    zip_code.county,
    concat(county_to_fips_mapping.state_fips, county_to_fips_mapping.county_fips) AS fips,
    bubble_tea.phone,
    bubble_tea.latitude,
    bubble_tea.longitude,
    bubble_tea.rating,
    bubble_tea.review_count
FROM bubble_tea
LEFT JOIN zip_code ON 1=1
    AND bubble_tea.zip_code = zip_code.zip
LEFT JOIN county_to_fips_mapping ON 1=1
    AND zip_code.county = county_to_fips_mapping.county;

CREATE OR REPLACE VIEW bubble_tea_w_hours AS
SELECT
    bubble_tea.id,
    bubble_tea.name,
    bubble_tea.country,
    bubble_tea.address1,
    bubble_tea.address2,
    bubble_tea.address3,
    bubble_tea.city,
    bubble_tea.state,
    bubble_tea.zip_code,
    bubble_tea.phone,
    bubble_tea.latitude,
    bubble_tea.longitude,
    bubble_tea.rating,
    bubble_tea.review_count,
    hours.day,
    hours.start,
    hours.end,
    hours.is_overnight
FROM bubble_tea
LEFT JOIN hours ON 1=1
    AND bubble_tea.id = hours.bubble_tea_id;
