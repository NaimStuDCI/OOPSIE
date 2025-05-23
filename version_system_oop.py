import json
from datetime import datetime

class Version():

    def __init__(self, filename, comment):
        self.filename = filename
        self.comment = comment

class VersionManager:
    CONFIG_FILE = "warehouse_inventory.json"
    DIRECTORY = "./backups/"

    def __init__(self):
        self.history = self.read_backups()

    def read_backups(self):
        with open(self.CONFIG_FILE, "r") as json_file:
            versions = []
            version_dictionary = json.load(json_file)
            for version in version_dictionary.keys():
                versions.append(Version(version, version_dictionary[version]))
        return versions
    
    def write_backups(self):
        with open(self.CONFIG_FILE, "w") as json_file:
            versions = {}
            for version in self.history:
                versions[version.filename] = version.comment
            json.dump(versions, json_file, indent = 4)

    def print_backups(self):
        """Prints the history of backups in a readable format."""
        index = 0
        for version in self.history:
            index += 1
            timestamp = version.filename[0:-4][-14:]  # Extract timestamp
            dummy_date = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            timestamp = dummy_date.strftime("%d. %B %Y, %H:%M:%S")
            print(f"{index}: \"{version.comment}\" created at {timestamp}")

    
# testobject = Version("warehouse.csv", "comment")
# print(testobject.version_filename())

# testobject = VersionManager()
# for version in testobject.read_backups():
#     print(version.filename, version.comment)

# testobject.print_backups()