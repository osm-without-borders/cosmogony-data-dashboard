# cosmogony-data-dashboard

To show stats about the world [Cosmogony](https://github.com/osm-without-borders/cosmogony)

:construction::warning: This is a work in progress, and deeply connected to the Cosmogony output format. Follow on in [this issue](https://github.com/osm-without-borders/cosmogony/issues/4) :warning::construction:

## Country stats and tests

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
