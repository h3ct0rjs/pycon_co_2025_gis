import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Pycon IT 2025 cookbook""")
    return


@app.cell
def _():
    import duckdb
    import folium
    import geopandas as gpd
    import marimo as mo

    from duckdb.duckdb import DuckDBPyConnection
    from rasterstats import zonal_stats

    TILES = "Cartodb dark_matter"
    return DuckDBPyConnection, TILES, duckdb, folium, gpd, mo, zonal_stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Setup connection
    This creates an in-memory duckdb database and installs the required extensions: `spatial` and `httpfs`.

    The `DESCRIBE` tables SQL command shows the database is initially empty.
    """
    )
    return


@app.cell
def _(duckdb):
    conn = duckdb.connect()

    # Loading extensions.
    conn.sql("INSTALL spatial")
    conn.sql("INSTALL httpfs")
    conn.sql("LOAD spatial")
    conn.sql("LOAD httpfs")

    conn.sql("DESCRIBE tables")
    return (conn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Vector data

    Vector data is spatial data, generally consisting of two parts: 

    * Geometry
    * Attributes

    **Geometries** are the *Points, Lines and Polygons*. They represent the "shape" of the real-world phenomenon. 
    **Attribute** data is information appended to the Geometry (or the other way around) 
    usually in tabular format ("records"). Together, this combination Geometry+Attributes 
    is often called a (Spatial) **Feature**.
    """
    )
    return


@app.cell
def _(conn):
    conn.sql("SELECT ST_POINT(0.0, 0.0) AS geom")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""You can perform geospatial operations over the geometry column. Please check https://duckdb.org/docs/stable/extensions/spatial/functions.html for the complete list of available functions""")
    return


@app.cell
def _(conn):
    conn.sql(
        """
        WITH geom_query AS (
            SELECT ST_POINT(0.0, 0.0) AS geom
        ) SELECT ST_AREA(geom) AS area, ST_LENGTH(geom) AS length, geom FROM geom_query
    """
    )
    return


@app.cell
def _(conn):
    conn.sql(
        """
        WITH geom_query AS (
            SELECT ST_MakeLine([ST_Point(0, 0), ST_Point(3, 4)]) AS geom
        ) SELECT ST_AREA(geom) AS area, ST_LENGTH(geom) AS length, geom FROM geom_query
    """
    )
    return


@app.cell
def _(conn):
    conn.sql(
        """
        WITH geom_query AS (
            SELECT ST_MakePolygon(ST_MakeLine([ST_Point(0, 0), ST_Point(1, 0), ST_Point(1, 1), ST_Point(0, 0)])) AS geom
        ) SELECT ST_AREA(geom) AS area, ST_LENGTH(geom) AS length, geom FROM geom_query
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Load simple CSV file""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can use Duckdb generic functions to load data from either remote or local files. However, make sure to create the tables properly within the in-memory database""")
    return


@app.cell
def _(conn):
    csv_file = "./col_relative_wealth_index.csv"

    # Works also with remote paths.
    # csv_file = "https://data.humdata.org/dataset/76f2a2ea-ba50-40f5-b79c-db95d668b843/resource/c0cfe555-a034-4716-9b50-ce9f70d186c0/download/col_relative_wealth_index.csv"
    conn.sql(f"SELECT * FROM read_csv('{csv_file}')")
    return (csv_file,)


@app.cell
def _(conn, csv_file):
    conn.sql(
        f"CREATE OR REPLACE TABLE 'rwi' AS SELECT * FROM read_csv('{csv_file}')"
    )
    conn.sql("DESCRIBE tables")
    return


@app.cell
def _(conn):
    conn.sql("DESCRIBE rwi")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The issue is that the created table in the csv file does not have the correct geometry column. You can fix this by creating the point geometry function""")
    return


@app.cell
def _(mo):
    mo.md(r"""### Create a geospatial table with geometry column""")
    return


@app.cell
def _(conn, csv_file):
    conn.sql(
        f"CREATE OR REPLACE TABLE 'rwi' AS SELECT rwi, error, ST_POINT(longitude, latitude) AS geom FROM read_csv('{csv_file}')"
    )
    conn.sql("SELECT * from rwi")
    return


@app.cell
def _(conn):
    conn.sql("SELECT geom FROM rwi LIMIT 2")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Geospatial formats for vector data

    There are currently [over 100 vector data formats](https://gdal.org/drivers/vector/index.html) used for storage, e.g. files, and for data transfer
    """
    )
    return


@app.cell
def _(conn):
    conn.sql("SELECT short_name, long_name FROM ST_DRIVERS()")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### GeoJSON

    [GeoJSON](https://geojson.org) is a simple JSON-based format to encode vector Features. 
    It is increasingly popular, especially among web developers. It is also the default data-format within
    the new [OGC REST APIs](https://ogcapi.ogc.org/) like [OGC API Features](https://ogcapi.ogc.org/features/).

    Example:

    ```
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
      },
      "properties": {
        "name": "Dinagat Islands"
        "population": 4785
      }
    }
    ```

    GitHub is able to display [GeoJSON-encoded data on-the-fly](https://github.com/jachym/jrdata/blob/master/jsons/stops.geojson).
    Note that coordinates are always in "easting, northing", thus longitude, latitude here.
    The use of alternative coordinate reference systems was
    removed from an earlier version of the [GeoJSON specification](https://datatracker.ietf.org/doc/html/rfc7946).
    However: "*...where all involved parties have a prior arrangement, alternative coordinate reference systems can be used without risk of data being misinterpreted.*"
    OGC is currently drafting [JSON-FG](https://docs.ogc.org/DRAFTS/21-045.html), GeoJSON extensions like Coordinate Reference Systems (CRS) support.

    ### ESRI Shapefile

    [ESRI Shapefile](https://en.wikipedia.org/wiki/Shapefile) is a file-based format. It consists of at least 3 files:

    * `.shp` containing geometry
    * `.shx` containing index
    * `.dbf` attribute table

    The ESRI Shapefile is one of the oldest formats, some even call it a [Curse in Geoinformatics](https://www.slideshare.net/jachym/switch-from-shapefile), and is more and more replaced by GeoPackage.

    ### Geography Markup Language (GML)

    > The Geography Markup Language (GML) is the XML grammar defined by the Open Geospatial Consortium (OGC) 
    > to express geographical features. GML serves as a modeling language for geographic 
    > systems as well as an open interchange format for geographic transactions on the Internet. Source: [Wikipedia](https://en.wikipedia.org/wiki/Geography_Markup_Language).

    Below an example of the same feature we saw earlier as GeoJSON, now in GML:

    ```
    <gml:featureMember>
      <feature fid="12">
        <id>23</id>
        <name>Dinagat Islands</name>
        <population>4785</population>
        <ogr:geometry>
          <gml:Point gml:id="p21" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">
            <gml:pos srsDimension="2">125.6, 10.1</gml:pos>
          </gml:Point>
        </ogr:geometry>
      </feature>
    </gml:featureMember>
    ```
    """
    )
    return


@app.cell
def _(conn):
    remote_url = "https://raw.githubusercontent.com/WFP-VAM/prism-app/refs/heads/master/frontend/public/data/colombia/col_municipios.json"
    conn.sql(
        f"""CREATE OR REPLACE TABLE 'boundaries_adm2' AS
        SELECT * EXCLUDE (DPTO_CNMBR, MPIO_CNMBR),
            MPIO_CNMBR AS ADM2_NAME,
            DPTO_CNMBR AS ADM1_NAME
        FROM ST_READ('{remote_url}')
    """
    )

    remote_url = "https://raw.githubusercontent.com/WFP-VAM/prism-app/refs/heads/master/frontend/public/data/colombia/admin-boundary-unified-polygon.json"
    conn.sql(
        f"""CREATE OR REPLACE TABLE 'boundaries_adm0' AS
        SELECT * FROM ST_READ('{remote_url}')
    """
    )
    return


@app.cell
def _(conn):
    conn.sql("DESCRIBE boundaries")
    return


@app.cell(hide_code=True)
def _(DuckDBPyConnection, gpd):
    def update_geometry_column(
        df: gpd.GeoDataFrame, column_name: str
    ) -> gpd.GeoDataFrame:
        df[column_name] = gpd.GeoSeries.from_wkt(df[column_name])
        gdf = gpd.GeoDataFrame(df, crs="EPSG:4326", geometry=column_name)

        return gdf

    def get_gdf(conn: DuckDBPyConnection, query: str) -> gpd.GeoDataFrame:
        df = conn.sql(query).df()
        gpd = update_geometry_column(df, "geometry")

        return gpd

    return (get_gdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Operations over attributes

    We can perform operations for all columns available in the dataset. For example, we can filter the administrative boundaries matching a given name.
    """
    )
    return


@app.cell
def _(conn):
    conn.sql("SELECT count(*) from boundaries where ADM1_NAME = 'ANTIOQUIA'")
    return


@app.cell
def _(conn):
    conn.sql("SELECT count(*) from rwi where rwi < 0")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Data visualization

    Now, we are going to run a query and transform the data into a geojson feature collection using the custom function _make_feature_collection_. Then, we use the folium library to display it in the notebook, centering it in Colombia and displaying the relative wealth index points as a geospatial layer.

    A webmap can be shown as a basemap, together with a list of layers stacked one over another.
    """
    )
    return


@app.cell
def _(conn, mo):
    _admin2_names = {
        f[0].capitalize(): f[0]
        for f in conn.sql(
            "SELECT ADM2_NAME FROM boundaries ORDER BY ADM2_NAME limit 1000"
        ).fetchall()
    }

    admin2_dropdown = mo.ui.dropdown(
        options=_admin2_names,
        label="choose one",
        searchable=True,
        value="Barranquilla",
    )

    _admin1_names = {
        f[0].capitalize(): f[0]
        for f in conn.sql(
            "SELECT ADM1_NAME FROM boundaries ORDER BY ADM1_NAME"
        ).fetchall()
    }

    admin1_dropdown = mo.ui.dropdown(
        options=_admin1_names,
        label="choose one",
        searchable=True,
        value="Caldas",
    )

    return admin1_dropdown, admin2_dropdown


@app.cell
def _(TILES, conn, folium, get_gdf):
    query = f"SELECT * EXCLUDE geom, ST_ASTEXT(geom) AS geometry from boundaries_adm2"

    map = folium.Map(tiles=TILES, min_zoom=5, location=(10.982781372175843, -74.82745259291546))
    rwi_gdf = get_gdf(
        conn, "SELECT rwi, ST_ASTEXT(geom) AS geometry FROM rwi limit 3000"
    )
    adm1_gdf = get_gdf(conn, query)
    folium.GeoJson(adm1_gdf, layer_name="boundaries").add_to(map)
    folium.GeoJson(rwi_gdf, layer_name="rwi", marker=folium.Circle()).add_to(map)
    map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Exploring geospatial relations

    It becomes also possible to perform spatial operations for the geometry column. The following query will find all the points that are within the filtered administrative boundary.

    <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/TopologicSpatialRelarions2.png" width="500" height="500" />
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### Find points within polygon""")
    return


@app.cell
def _(admin2_dropdown):
    admin2_dropdown
    return


@app.cell
def _(TILES, admin2_dropdown, conn, folium, get_gdf):
    boundary_query = f"SELECT * EXCLUDE geom, ST_ASTEXT(geom) AS geometry from boundaries WHERE ADM2_NAME = '{admin2_dropdown.value}'"
    boundary_gdf = get_gdf(conn, boundary_query)

    location = conn.sql(
        f"""
        WITH t1 AS (
            SELECT ST_CENTROID(geom) AS pt  from boundaries where ADM2_NAME = '{admin2_dropdown.value}'
        ) SELECT ST_Y(pt), ST_X(pt) FROM t1
    """
    ).fetchone()

    _query = f"""
        WITH selected_boundary AS (
            SELECT geom FROM boundaries WHERE ADM2_NAME = '{admin2_dropdown.value}'
        )
        SELECT
            rwi.rwi,
            ST_ASTEXT(rwi.geom) AS geometry
        FROM rwi, selected_boundary
        WHERE ST_WITHIN(rwi.geom, selected_boundary.geom)
    """

    _map = folium.Map(tiles=TILES, min_zoom=7, location=location)

    filtered_gdf = get_gdf(conn, _query)
    folium.GeoJson(boundary_gdf, layer_name="boundary").add_to(_map)
    folium.GeoJson(filtered_gdf, layer_name="rwi", marker=folium.Circle()).add_to(_map)
    _map

    return (location,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Projection

    <img src="https://bok-figures.s3.amazonaws.com/files/figure2-projections.png" width="600" height="500"/>
    """
    )
    return


@app.cell
def _(admin2_dropdown):
    admin2_dropdown
    return


@app.cell
def _(TILES, admin2_dropdown, conn, folium, get_gdf, location):
    _query = f"""
        WITH selected_boundary AS (
            SELECT geom FROM boundaries WHERE ADM2_NAME = '{admin2_dropdown.value}'
        ), intersected_rwi AS (
            SELECT rwi.rwi, rwi.geom AS geom FROM rwi, selected_boundary WHERE ST_INTERSECTS(rwi.geom, selected_boundary.geom)
        ), buffered_points AS (
            SELECT 
                rwi,
                -- Transform to wgs84 with units in degrees.
                ST_TRANSFORM(
                    -- Create small squares buffer
                    ST_BUFFER(
                        -- Tranform to Colombia projection in meters.
                        ST_TRANSFORM(geom, 'EPSG:4326', 'EPSG:32619', true),
                    1200, 16, 'CAP_SQUARE', 'JOIN_ROUND', 1.0),
                'EPSG:32619',
                'EPSG:4326',
                true
                ) AS geom FROM intersected_rwi
                WHERE rwi < 0
        ) SELECT ST_ASTEXT(geom) AS geometry FROM buffered_points
    """

    _map = folium.Map(tiles=TILES, min_zoom=12, location=location)

    _filtered_gdf = get_gdf(conn, _query)
    folium.GeoJson(_filtered_gdf, layer_name="rwi", marker=folium.Circle()).add_to(_map)
    _map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Combined operations between raster and vector data. Zonal statistics

    <img src="https://rfsaldanha.github.io/brclimr/articles/images/zonal_statistics.png" />

    As the figure shown above, zonal statistics is a process that receives a layer with polygons and a raster file. Then for each polygon, the algorithm creates the spatial intersection and computes statistics using the values within the intersected pixels. For this presentation, we will make use of the population raster from [Worldpop](https://hub.worldpop.org/geodata/summary?id=25805)
    """
    )
    return


@app.cell
def _(admin1_dropdown):
    admin1_dropdown
    return


@app.cell
def _(admin1_dropdown, conn, zonal_stats):
    def apply_zonal_stats(
        geoms: list[str], population_raster_path: str
    ) -> int:
        results = zonal_stats(geoms, population_raster_path, stats=["sum"])
        total_count = sum([r["sum"] for r in results])
        return int(total_count)

    if conn.execute("SELECT * from duckdb_functions() WHERE function_name = 'apply_zonal_stats'").fetchone() is None:
        conn.create_function("apply_zonal_stats", apply_zonal_stats)


    _query = f"""
        WITH selected_boundary AS (
            SELECT ADM2_NAME AS adm_name, geom FROM boundaries WHERE ADM1_NAME = '{admin1_dropdown.value}'
        ), intersected_rwi AS (
            SELECT selected_boundary.adm_name, rwi.rwi, rwi.geom AS geom FROM rwi, selected_boundary WHERE ST_INTERSECTS(rwi.geom, selected_boundary.geom)
        ), buffered_points AS (
            SELECT 
                adm_name,
                ST_TRANSFORM(
                    ST_BUFFER(ST_TRANSFORM(geom, 'EPSG:4326', 'EPSG:32619', true), 2400, 16, 'CAP_SQUARE', 'JOIN_ROUND', 1.0),
                    'EPSG:32619',
                    'EPSG:4326',
                    true
                ) AS geom FROM intersected_rwi
                WHERE rwi < 0

        -- IMPORTANT PART OF QUERY.

        ), grouped_admins AS (
            SELECT adm_name, ARRAY_AGG(ST_ASTEXT(geom)) AS geometries FROM buffered_points GROUP BY adm_name
        ) SELECT adm_name, apply_zonal_stats(geometries, './col_ppp_2020_1km_Aggregated_UNadj.tif') AS count_stats FROM grouped_admins
    """

    conn.sql(_query)
    return


if __name__ == "__main__":
    app.run()
