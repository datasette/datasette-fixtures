from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-fixtures" in installed_plugins


@pytest.mark.asyncio
async def test_plugin_creates_populated_fixtures_database():
    datasette = Datasette()
    await datasette.invoke_startup()

    db = datasette.get_database("fixtures")
    assert db.is_memory
    assert (await db.execute("select count(*) from facetable")).first()[0] > 5
    assert (await db.execute("select count(*) from binary_data")).first()[0] > 1
