from csv import DictReader
from os import listdir
from typing import Iterator, Iterable
from dataclasses import dataclass
from psycopg import Cursor
import psycopg
from psycopg.sql import SQL


# building_id,region,municipality,street,house_number,postal_code,latitude_wgs84,longitude_wgs84,building_use
# 100004107X,01,257,"Kurkistontie",149,02880,60.265311,24.414921,2
@dataclass(frozen=True)
class Address:
    postal_code: str
    address: str


def upsert_addresses(
        cursor: Cursor,
        addresses: Iterable[Address],
) -> None:
    insert_sql = SQL("""
        INSERT INTO address (
            postal_code,
            address
        ) VALUES (
            %(postal_code)s,
            %(address)s
        ) ON CONFLICT (postal_code, address) DO NOTHING;
    """)

    cursor.executemany(
        insert_sql,
        (a.__dict__ for a in addresses),
    )


def get_addresses() -> Iterable[Address]:
    data_dir = "data/finland_addresses_2024-08-14_json/data/"
    for csv_file in listdir(data_dir):
        with open(data_dir + csv_file) as csv:
            reader = DictReader(csv)
            for row in reader:
                yield Address(
                    postal_code=row["postal_code"],
                    address=f"{row['street']} {row['house_number']}"
                )


if __name__ == '__main__':
    with psycopg.connect("host=localhost dbname=possu user=postgres password=postgres") as conn, \
            conn.cursor() as cur:
        upsert_addresses(cur, get_addresses())
        conn.commit()
