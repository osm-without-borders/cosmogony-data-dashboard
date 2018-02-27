# coding: utf-8

import pandas as pd
import json
import csv
import pytest

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
    # you can then launch via py.test, using the dumped csv file
    if line['test_status'] == "skip":
        pytest.skip("no data for this test")
    assert(line['test_status'] == "ok"), "Country {} - expected between {} and {} for {}, found {}".format(
        line['name'], line['expected_min'], line['expected_max'], line['zone_type'], line['total'])


cascading_child_types = ['state', 'state_district', 'city', 'suburb']

with open('fr.json', 'r') as file_i: # TODO
    tt = json.load(file_i)
    zones_ = tt['zones']
zones = pd.DataFrame(zones_)

volumetries = []

countries = zones[zones['zone_type'] == "country"]
wikidata_countries = list(zones['wikidata'])

for wikidata_country_id in wikidata_countries:
    country = zones[zones['wikidata'] == wikidata_country_id]
    if not len(country):
        continue
    country_id = int(country.head(1)['id'])
    parent_id_list = [country_id]

    for child_type in cascading_child_types:
        childs = extract_childs(zones, child_type, parent_id_list)
        nb_childs = len(childs)
        volumetries.append({'zone_type': child_type,
                            'total': nb_childs, 'wikidata_id': wikidata_country_id})
        if nb_childs:
            parent_id_list += list(childs['id'])


#dump_volumetries(volumetries, "lux_volumetries.csv")
expected_values = pd.read_csv('reference_stats_values.csv')
actual_values = pd.DataFrame(volumetries)
merged = pd.merge(expected_values, actual_values, on=[
                  'wikidata_id', 'zone_type'], how='left')
merged.fillna(-1, inplace=True)
merged['test_status'] = list(map(lambda expected_min, expected_max, total: check_if_test_passes(
    expected_min, expected_max, total), merged['expected_min'], merged['expected_max'], merged['total']))
merged.to_csv('data_volumetric.csv')
merged.to_json('data_volumetric.json', orient='records')
