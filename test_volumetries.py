# coding: utf-8

import pandas as pd
import geopandas
import json
import csv
import pytest


def dump_cosmogony_to_geojson(cosmogony_file_name):
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    zones = []

    with open(cosmogony_file_name, 'r') as file_i:
        tt = json.load(file_i)
        zones = tt['zones']

    geojson['features'] = [{
        'type': 'Feature',
        'geometry': a_zone['geometry'],
        'properties': {key: value for key, value in a_zone.items() if key != 'geometry'}
    } for a_zone in zones]

    with open('cosmogony.geojson', 'w') as file_o:
        json.dump(geojson, file_o)


def extract_childs(all_zones, child_type, parents_id):
    childs = all_zones[all_zones['zone_type'] == child_type]
    childs_to_keep = childs[childs['parent'].isin(parents_id)]
    return childs_to_keep


def dump_volumetries(volumetries, file_name):
    headers = ['wikidata_id', 'zone_type', 'total']
    with open(file_name, 'w') as f:
        dw = csv.DictWriter(f, delimiter=',', fieldnames=headers)
        dw.writeheader()
        for row in volumetries:
            dw.writerow(row)


def check_if_test_passes(expected_min, expected_max, total):
    if total == -1:
        return "skip"
    if expected_min <= total and expected_max >= total:
        return "ok"
    else:
        return "ko"

def test_row(line):
    #you can then launch via py.test, using the dumped csv file
    if line['test_status'] == "skip":
        pytest.skip("no data for this test")
    assert(line['test_status'] == "ok")

cascading_child_types = ['state', 'state_district', 'city', 'suburb']

wikidata_country_id = 'Q32'  # TODO
dump_cosmogony_to_geojson('cosmogony_lux.json')  # TODO

zones = geopandas.read_file('cosmogony.geojson', driver='GeoJSON')

volumetries = []
country = zones[zones['wikidata'] == wikidata_country_id]
country_id = int(country.head(1)['id'])
parent_id_list = [country_id]

for child_type in cascading_child_types:
    childs = extract_childs(zones, child_type, parent_id_list)
    nb_childs = len(childs)
    volumetries.append({'zone_type': child_type,
                        'total': nb_childs, 'wikidata_id': wikidata_country_id})
    if nb_childs:
        parent_id_list += list(childs['id'])


#dump_volumetries(volumetries, "lux_volumetries.cs")
expected_values = pd.read_csv('reference_stats_values.csv')
actual_values = pd.DataFrame(volumetries)
merged = pd.merge(expected_values, actual_values, on=[
                  'wikidata_id', 'zone_type'], how='left')
merged.fillna(-1, inplace=True)
merged['test_status'] = list(map(lambda expected_min, expected_max, total: check_if_test_passes(
    expected_min, expected_max, total), merged['expected_min'], merged['expected_max'], merged['total']))
#merged.to_csv('data_volumetric.csv')
merged.to_json('data_volumetric.json', orient='records')
