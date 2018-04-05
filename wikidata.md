# wikidata

These are just a few sparql magic to compare your cosmogony with [wikidata](https://query.wikidata.org).

## Get the list of zones with some administrative zones type

```sql
SELECT distinct ?item ?itemLabel ?geoLoc WHERE {
  ?item (wdt:P31/wdt:P279*) wd:Q6465.
  ?item wdt:P625 ?geoLoc.
  OPTIONAL {?item wdt:P576 ?fin.}
  OPTIONAL {?item wdt:P582 ?fin_autre.}
  OPTIONAL { ?item wdt:P2561 ?nom. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }
  FILTER(!BOUND(?fin))
  FILTER(!BOUND(?fin_autre))
 }
```

Replace `Q6465` (departments in France) with your administrative zone type of interest.

The column `wikidata_ontology` from reference stats values file contains a few ones.

Beware of the former zones, which may have some kind of `end time` statement or qualifier.

## Get wikidata ontology for some country

This returns the first-level administrative country subdivision, which may match the `state` zone type.

```sql
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P279 wd:Q10864048.
  ?item wdt:P17 wd:Q142.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

Replace Q142 (France) with your country of interest.

Q13220204 is the second-level administrative subdivision (which may match `state_district`).
