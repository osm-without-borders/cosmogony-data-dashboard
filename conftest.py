# coding: utf-8
import pandas as pd

from utils import ZonesIndex, CONFIG


def pytest_addoption(parser):
    parser.addoption("--cosmogony", action="store", required=True,
        help="a cosmogony json file")
    parser.addoption("--output", action="store", default='data_volumetric.json',
        help="path to result file")

def pytest_configure(config):
    CONFIG['output'] = config.getoption('--output')

def pytest_generate_tests(metafunc):
    cosmogony_path = metafunc.config.getoption('cosmogony')
    zones_index = ZonesIndex.init_from_cosmogony(cosmogony_path)

    expected_values = pd.read_csv('reference_stats_values.csv')
    rows = (row for idx,row in expected_values.iterrows())

    if 'line' in metafunc.fixturenames:
        metafunc.parametrize('line', rows)
    if 'zones_index' in metafunc.fixturenames:
        metafunc.parametrize('zones_index', [zones_index])
