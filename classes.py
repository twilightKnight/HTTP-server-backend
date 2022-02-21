class CityObject:
    """Class storing all information about city"""

    def __init__(self, datalist: list):
        self.geonameid, \
            self.name, \
            self.asciiname, \
            self.alternatenames, \
            self.latitude, \
            self.longitude, \
            self.feature_class, \
            self.feature_code, \
            self.country_code, \
            self.cc2, \
            self.admin1_code, \
            self.admin2_code, \
            self.admin3_code, \
            self.admin4_code, \
            self.population, \
            self.elevation, \
            self.dem, \
            self.timezone, \
            self.modification_date = datalist


class TimeZone:
    """Class storing time zones"""

    def __init__(self, time_zone_id, gmt_offset):
        self.time_zone_id = time_zone_id
        self.gmt_offset = gmt_offset
