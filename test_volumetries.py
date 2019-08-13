# coding: utf-8
import pandas as pd
import pytest

from utils import UnknownWikidataId, CONFIG

def check_if_test_passes(expected_min, expected_max, total):
    if expected_min <= total <= expected_max:
        return "ok"
    else:
        return "ko"

class TestCosmogony:
    @classmethod
    def setup_class(cls):
        cls.results = pd.DataFrame()

    @classmethod
    def teardown_class(cls):
        cls.results.to_json(CONFIG['output'], orient='records')

    def test_row(self, line, zones_index):
        try:
            matched_zones = list(zones_index.iter_children(
                line['wikidata_id'],
                lambda z:z['zone_type']==line['zone_type']
            ))
        except UnknownWikidataId:
            total = -1
            test_status = 'skip'
        else:
            total = len(matched_zones)
            test_status = check_if_test_passes(line.expected_min, line.expected_max, total)

        line['total'] = total
        line['test_status'] = test_status
        TestCosmogony.results = TestCosmogony.results.append(line)

        if test_status == 'skip':
            pytest.skip("no data for this test")

        assert(test_status == "ok"), "Country {} - expected between {} and {} for {}, found {}".format(
            line['name'], line['expected_min'], line['expected_max'], line['zone_type'], total)
