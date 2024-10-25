CREATE TABLE address
(
    address     TEXT,
    postal_code TEXT NOT NULL,
    CONSTRAINT address_pk PRIMARY KEY (postal_code, address)
);

ALTER TABLE address
ADD COLUMN search tsvector
GENERATED ALWAYS AS (to_tsvector('english', postal_code || ' ' || address)) STORED;

CREATE INDEX address_search_idx
	ON address
	USING gin (search);


