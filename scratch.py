import datetime,gzip,pickle,os,sys,struct

class Incident:
    def __init__(self, report_id, date, airport, aircraft_id,
                 aircraft_type, pilot_percent_hours_on_type,
                 pilot_total_hours, midair, narrative=""):
        assert len(report_id) >= 8 and len(report_id.split()) == 1, "invalid report ID"
        self.report_id = report_id
        self.date = date
        self.airport = airport
        self.aircraft_id = aircraft_id
        self.aircraft_type = aircraft_type
        self.pilot_percent_hours_on_type = pilot_percent_hours_on_type
        self.pilot_total_hours = pilot_total_hours
        self.midair = midair
        self.narrative = narrative

    @property
    def date(self):
        return self.__date


    @date.setter
    def date(self, date):
        assert isinstance(date, datetime.date), "invalid date"
        self.__date = date


class IncidentCollections(dict):
    def values(self):
        for report_id in self.keys():
            yield self[report_id]

    def items(self):
        for report_id in self.keys():
            yield (report_id, self[report_id])

    def __iter__(self):
        for report_id in sorted(super.keys()):
            yield report_id

    key = __iter__

    def export_pickle(self, filename,compress = False):
        fh = None
        try:
            if compress:
                fh = gzip.open(filename,"wb")
            else:
                fh = open(filename,  "wb")
            pickle.dump(self, fh, pickle.HIGHEST_PROTOCOL)
            return True
        except (EnvironmentError, pickle.UnpicklingError) as err:
            print("{0}: export error: {1}".format(
                os.path.basename(sys.argv[0]), err))
            return False
        finally:
            if fh is not None:
                fh.close()

            GZIP_MAGIC = b"\x1F\x8B"

    def import_pickle(self, filename):
        GZIP_MAGIC = b"\x1F\x8B"
        fh = None
        try:
            fh = open(filename, "rb")
            magic = fh.read(len(GZIP_MAGIC))
            if magic == GZIP_MAGIC:
                fh.close()
                fh = gzip.open(filename, "rb")
            else:
                fh.seek(0)
            self.clear()
            self.update(pickle.load(fh))
            return True
        except (EnvironmentError, pickle.UnpicklingError) as err:
            print("{0}: import error: {1}".format(
            os.path.basename(sys.argv[0]), err))
            return False
        finally:
            if fh is not None:
                fh.close()
        MAGIC = b"AIB\x00"
        FORMAT_VERSION = b"\x00\x01"

    def export_binary(self, filename, compress = False):
        print("eerre")
        MAGIC = b"AIB\x00"
        FORMAT_VERSION = b"\x00\x01"
        def pack_string(string):
            data = string.encode("utf8")
            format = "<H{0}s".format(len(data))
            return struct.pack(format, len(data), data)
        fh = None
        try:
            if compress:
                fh = gzip.open(filename, "wb")

            else:
                fh = open(filename, "wb")
            fh.write(MAGIC)
            fh.write(FORMAT_VERSION)
            NumbersStruct = struct.Struct("<Idi?")
            for incident in self.values():
                data = bytearray()
                data.extend(pack_string(incident.report_id))
                data.extend(pack_string(incident.airport))
                data.extend(pack_string(incident.aircraft_id))
                data.extend(pack_string(incident.aircraft_type))
                data.extend(pack_string(incident.narrative.strip()))
                data.extend(NumbersStruct.pack(
                    incident.date.toordinal(),
                    incident.pilot_percent_hours_on_type,
                    incident.pilot_total_hours,
                    incident.midair
                ))
            fh.write(data)
        except Exception as err:
            print(err)
        return True

    def import_binary(self, filename):
        print("4343")
        NumbersStruct = struct.Struct("<Idi?")
        def unpack_string(fh, eof_is_error=True):
            print(eof_is_error)
            uint16 = struct.Struct("<H")
            length_data = fh.read(uint16.size)
            print("yes", length_data,87)

            if not length_data:
                if eof_is_error:
                    raise ValueError("missing or corrupt string size")
                return 78

            length = uint16.unpack(length_data)[0]
            print(length, "2343")
            if length == 0:
                return ""
            data = fh.read(length)
            print(data,"re")
            print(data,"me",len(data),length,len(data) != length)
            if not data or len(data) != length:
                raise ValueError("missing or corrupt string")
            format = "<{0}s".format(length)
            return struct.unpack(format, data)[0].decode("utf8")

        fh = None
        MAGIC = b"AIB\x00"
        FORMAT_VERSION = b"\x00\x01"
        GZIP_MAGIC = b"\x1F\x8B"
        try:
            fh = open(filename, "rb")
            magic = fh.read(len(GZIP_MAGIC))
            if magic == GZIP_MAGIC:
                fh.close()
                fh = gzip.open(filename, "rb")
            else:
                fh.seek(0)
            magic = fh.read(len(MAGIC))
            if magic != MAGIC:
                raise ValueError("invalid .aib file format")
            version = fh.read(len(FORMAT_VERSION))
            if version > FORMAT_VERSION:
                raise ValueError("unrecognized .aib file version")
            self.clear()
        except Exception as err:
            print(err)

        while True:
            report_id = unpack_string(fh, False)
            if report_id is None:
                break
            data = {}
            data["report_id"] = report_id
            for name in ("airport", "aircraft_id",
                         "aircraft_type", "narrative"):
                data[name] = unpack_string(fh)
                print(data[name],34)
                other_data = fh.read(NumbersStruct.size)
            numbers = NumbersStruct.unpack(other_data)
            data["date"] = datetime.date.fromordinal(numbers[0])
            data["pilot_percent_hours_on_type"] = numbers[1]
            data["pilot_total_hours"] = numbers[2]
            data["midair"] = numbers[3]
            incident = Incident(**data)
            self[incident.report_id] = incident
            print(89)
        return True
z = IncidentCollections()
z[0] = Incident("03434343",datetime.datetime.now(),"heathr","bone", "erereded",90,midair=True,pilot_total_hours=99900)
z.export_binary(r"C:\Users\DAVID\.PyCharmCE2019.1\config\scratches\me.bin")
print(z.import_binary(r"C:\Users\DAVID\.PyCharmCE2019.1\config\scratches\me.bin"))