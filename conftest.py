# coding: utf-8

import csv
import test_volumetries


def pytest_generate_tests(metafunc):
    with open('data_volumetric.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        rows = list(csvreader)
        if 'line' in metafunc.fixturenames:
            metafunc.parametrize('line', rows)
