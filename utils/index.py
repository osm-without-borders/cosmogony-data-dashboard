import typing
from collections import defaultdict
import gzip
import json
import ijson.backends.yajl2_cffi as ijson

CONFIG = {
    'output': None,
}

class UnknownWikidataId(Exception):
    pass

class ZonesIndex:
    """
    Index cosmogony zones both by internal `id` and wikidata id
    """
    @classmethod
    def init_from_cosmogony(cls, cosmogony_path: str):
        zones_index = cls()

        def index_zones(zones: typing.Iterable[dict]):
            for z in zones:
                z.pop('geometry', None)
                zones_index.insert(z)

        print('Reading zones...')
        if cosmogony_path.endswith('.json'):
            with open(cosmogony_path, 'rb') as f:
                zones = ijson.items(f, 'zones.item')
                index_zones(zones)
        elif cosmogony_path.endswith('.jsonl.gz'):
            with gzip.open(cosmogony_path) as f:
                zones = (json.loads(line) for line in f)
                index_zones(zones)
        else:
            raise Exception("Unknown file extension in '{}'", cosmogony_path)

        print('{} zones have been read'.format(len(zones_index)))

        zones_index.build_children()
        return zones_index

    def __init__(self):
        self.id_to_zone = dict()
        self.wd_to_zone = dict()
        self.id_to_children = defaultdict(list)

    def insert(self, zone):
        self.id_to_zone[zone['id']] = zone
        wikidata_id = zone.get('wikidata')
        if wikidata_id:
            self.wd_to_zone[wikidata_id] = zone

    def build_children(self):
        for z in self.id_to_zone.values():
            parent_id = z.get('parent')
            if parent_id is not None:
                self.id_to_children[parent_id].append(z)

    def _iter_all_children(self, zone):
        children = self.id_to_children[zone['id']]
        for c in children:
            yield c
            yield from self._iter_all_children(c)

    def iter_children(self, wikidata_id, filter_fun=lambda x: True):
        try:
            zone = self.wd_to_zone[wikidata_id]
        except KeyError as e:
            raise UnknownWikidataId from e

        return filter(filter_fun, self._iter_all_children(zone))

    def __len__(self):
        return len(self.id_to_zone)
