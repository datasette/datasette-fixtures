from datasette import hookimpl
from datasette.fixtures import populate_fixture_database


@hookimpl
def startup(datasette):
    async def inner():
        if "fixtures" in datasette.databases:
            db = datasette.get_database("fixtures")
        else:
            db = datasette.add_memory_database("fixtures", name="fixtures")

        def populate_if_empty(conn):
            if not conn.execute("select count(*) from sqlite_master").fetchone()[0]:
                populate_fixture_database(conn)

        await db.execute_write_fn(populate_if_empty)

    return inner
