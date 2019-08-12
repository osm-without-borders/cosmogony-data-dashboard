# cosmogony-data-dashboard

The purpose of this repo is to provide tools to compute and show stats about the world [Cosmogony](https://github.com/osm-without-borders/cosmogony).

It can help to check the quality (well, mostly the quantity actually...) of OpenStreetMap boundaries zones.

Contributions are very welcomed in the repo. If you have new ideas about tests to add, please take a look at the [founding issue](https://github.com/osm-without-borders/cosmogony/issues/4) first ;)

:construction::warning: This is a work in progress, and deeply connected to the Cosmogony output format. Follow on in [this issue](https://github.com/osm-without-borders/cosmogony/issues/4) :warning::construction:

## Country stats and tests

### Purpose

We want to compute the number of zones for each kind of zone and for each country. Then, we want to compare this output with some references values (the actual number of zones for each kind of zone in the real world)

### Compute and test against references values

You will need `python3` and a few dependancies you can install with `pipenv install --three`.

To compute the number of zones for each kind of zones (volumetric stats) and test them again reference values, just type:

`pipenv run py.test --cosmogony=my-cosmogony.json`

Detailed test results are written to `data_volumetric.json`.

You can also get some visual results over the tests using the `index.html` file inside the repo.

### Reference values

For now, the references values is a big csv file.

| wikidata_id         | zone_type      | expected_min | expected_max | is_known_failure |
|----------------------|-------------------|-------------------|--------------------|-----------------------|
| Q142                | state          | 17           | 19           |                  |
| Q142                | state_district | 96           | 106          |                  |
| Q142                | city           | 35000        | 36000        |                  |
| Q142                | city_district  | 35000        | 36000        | yes              |

Expected min and max values are the number of administrative zones that are expected, according to official sources.

If this number is known but OSM data are not yet up to date, you can flag the tests as a known failure.

Cosmogony, just like OpenStreetMap, emphasizes local knowledge: feel free to add some numbers for the countries you know about ;)
[Learn more here](https://github.com/osm-without-borders/cosmogony#contribute)
