import json, os, shutil
from datetime import datetime
from userauth import authenticate_user

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
    
    def create_copie(self, filename):
        """Creates a copy of the file with a timestamp."""
        new_filename = filename[0:-4] + datetime.now().strftime("%Y%m%d%H%M%S" + ".csv")
        if os.path.exists(filename):
            shutil.copy(filename, f"{self.DIRECTORY}{new_filename}")
        return new_filename
    
    def update_backups(self, filename, vscomment):
        """Updates the backup history with a new entry."""
        key_name = self.create_copie(filename)
        self.history.append(Version(key_name, vscomment))
        self.write_backups()
        self.print_backups()

    @authenticate_user
    def restore_version(self, filename):
        """Restores a version of the file from the backup history."""
        print("\n")
        
        self.print_backups()
        index = input("Enter the index of the backup you want to restore: ")
        while not index.isdigit():
            index = input("Enter the index of the backup you want to restore: ")
        index = int(index)
        if index < 1 or index > len(self.history):
            print("Invalid index. Please try again.")
            input()
            return
        version_filename = self.history[index - 1].filename
        self.update_backups(filename, f"restored from {version_filename}")
        shutil.copy(f"{self.DIRECTORY}{version_filename}", filename)


testobject = VersionManager()
for version in testobject.read_backups():
    print(version.filename, version.comment)

testobject.restore_version("warehouse_inventory.csv")
