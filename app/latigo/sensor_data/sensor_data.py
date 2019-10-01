from datetime import datetime
from latigo.sensor_data import *


class SensorDataProviderInterface:

    def get_data_for_range(self, time_range: TimeRange) -> SensorData:
        """
        return the actual data as per the range specified
        """
        pass


class MockSensorDataProvider(SensorDataProviderInterface):


    def get_data_for_range(self, time_range: TimeRange) -> SensorData:
        """
        return the actual data as per the range specified
        """
        data=SensorData()
        data.time_range=time_range

        return data
