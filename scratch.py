import datetime, gzip, pickle, os, sys, struct

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
        assert isinstance(date, datetime.date), "invalid date object"
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

    # key = __iter__

    def export_pickle(self, filename, compress=False):
        file = None
        try:
            if compress:
                file = gzip.open(filename,"wb")
            else:
                file = open(filename,  "wb")
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
            return True
        except (EnvironmentError, pickle.UnpicklingError) as err:
            print("{0}: export error: {1}".format(os.path.basename(sys.argv[0]),
                                                    err))
            return False
        finally:
            if file is not None:
                file.close()

    def import_pickle(self, filename):
        GZIP_MAGIC = b"\x1F\x8B"
        file = None
        try:
            file = open(filename, "rb")
            magic = file.read(len(GZIP_MAGIC))
            if magic == GZIP_MAGIC:
                file.close()
                file = gzip.open(filename, "rb")
            else:
                file.seek(0)
            self.clear()
            self.update(pickle.load(file))
            return True
        except (EnvironmentError, pickle.UnpicklingError) as err:
            print("{0}: import error: {1}".format(os.path.basename(sys.argv[0]),
                                                    err))
            return False
        finally:
            if file is not None:
                file.close()
        # MAGIC = b"AIB\x00"
        # FORMAT_VERSION = b"\x00\x01"

    def export_binary(self, filename, compress = False):
        print("Entering `export_binary`...")

        def pack_string(string):
            data = string.encode("utf8")
            format = "<H{0}s".format(len(data))
            return struct.pack(format, len(data), data)

        MAGIC = b"AIB\x00"
        FORMAT_VERSION = b"\x00\x01"
        file = None
        try:
            if compress:
                file = gzip.open(filename, "wb")
            else:
                file = open(filename, "wb")

            file.write(MAGIC)
            file.write(FORMAT_VERSION)

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

            file.write(data)
        except Exception as err:
            print(err)

        return True

    def import_binary(self, filename):
        print("Entering `import_binary`")

        def unpack_string(file, eof_is_error=False):
            print(f"Entering `unpack_string`... {eof_is_error= }")
            uint16 = struct.Struct("<H")
            length_data = file.read(uint16.size)
            print(f"{length_data= }")

            if not length_data:
                if eof_is_error:
                    raise ValueError("missing or corrupt string size")
                return None

            length = uint16.unpack(length_data)[0]
            print(f"{length= }")
            if not length:
                return ""

            data = file.read(length)
            print(f"{data= }")
            print(data, len(data), length)
            if len(data) != length:
                raise ValueError("missing or corrupt string")

            return struct.unpack(f"<{length}s", data)[0].decode("utf8")


        NumbersStruct = struct.Struct("<Idi?")
        file = None
        MAGIC = b"AIB\x00"
        FORMAT_VERSION = b"\x00\x01"
        GZIP_MAGIC = b"\x1F\x8B"

        # try:
        file = open(filename, "rb")
        magic = file.read(len(GZIP_MAGIC))
        if magic == GZIP_MAGIC:
            file.close()
            file = gzip.open(filename, "rb")
        else:
            file.seek(0)

        magic = file.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError("invalid .aib file format")

        version = file.read(len(FORMAT_VERSION))
        if version > FORMAT_VERSION:
            raise ValueError("unrecognized .aib file version")

        self.clear()
        # except Exception as err:
        #     print(err)

        data = {}
        while True:
            report_id = unpack_string(file, False)
            if report_id is None:  # End of data
                break
            data["report_id"] = report_id
            print(f"\n{report_id= }\n")

            for name in ("airport", "aircraft_id", "aircraft_type", "narrative"):
                data[name] = unpack_string(file)
                print(f"{name}= {data[name]!r}\n")

            other_data = file.read(NumbersStruct.size)
            numbers = NumbersStruct.unpack(other_data)
            data["date"] = datetime.date.fromordinal(numbers[0])
            data["pilot_percent_hours_on_type"] = numbers[1]
            data["pilot_total_hours"] = numbers[2]
            data["midair"] = numbers[3]

            incident = Incident(**data)
            self[report_id] = incident
            data.clear()


z = IncidentCollections()
z[0] = Incident("03434343",datetime.datetime.now(),"heathr","bone", "erereded",90,midair=True,pilot_total_hours=99900)
z.export_binary("./me.bin")
z.import_binary("./me.bin")

print(z)

