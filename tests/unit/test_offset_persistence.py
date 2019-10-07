from os import environ

# NOTE: This must be started befoer the imports
# Set up memory database (no file)
environ["LATIGO_INTERNAL_DATABASE"] = "sqlite://"

import logging
from latigo.event_hub.offset_persistence import DBOffsetPersistance, MemoryOffsetPersistance
from azure.eventhub import Offset

logger=logging.getLogger(__name__)

class TestOffsetPersistence:
    # https://stackoverflow.com/questions/58267623/how-can-i-store-azure-eventhub-common-offset-in-python
    def test_offset_serialization(self):
        ofs=Offset("0")
        logger.info(ofs)
        logger.info(ofs.selector())
        logger.info(ofs.__dict__)
        
    def test_get_set(self):
        for op in [MemoryOffsetPersistance(), DBOffsetPersistance("tester")]:
            # Test explicit default
            assert "bob" == op.get("bob")
            # Test implicit default
            assert "@latest" == op.get()
            # Test recollection of set value
            offset = "1337"
            op.set(offset)
            ret = op.get()
            assert ret == offset