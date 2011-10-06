--Table to store authentication and device strings

CREATE TABLE auth (
	id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
	username VARCHAR UNIQUE,
	password VARCHAR
);

CREATE TABLE devices (
	device_string VARCHAR NOT NULL PRIMARY KEY,
	userid INTEGER,
	_type VARCHAR,
	registered_ip VARCHAR,
	registered_time TIMESTAMP
);

CREATE TABLE messages (
	id INTEGER PRIMARY KEY,
	content TEXT,
	device_string VARCHAR,
	origin_ip VARCHAR,
	sent_time TIMESTAMP,
	queued_time TIMESTAMP,
	priority INTEGER,
	delivered SMALLINT
);
