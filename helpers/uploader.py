from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from helpers.constants import RESOURCES_PATH


class GDriveUploader:
    def __init__(self):
        # Create GoogleDrive instance with authenticated GoogleAuth instance.
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = RESOURCES_PATH + 'client_secret_861732897278-35g552go20trvgj7prjhogtkf84dj1s4.apps.googleusercontent.com.json'
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(RESOURCES_PATH + "mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(RESOURCES_PATH + "mycreds.txt")
        self.drive = GoogleDrive(gauth)

    def upload(self, file_name, file):
        print("Uploading ", file_name)
        gfolder_id = "1J3x3rxRZ4EEljGRVLIic1zmfYp4MO-Zw" # HIMO-2021 folder id
        file1 = self.drive.CreateFile({
            'title': file_name,
            "parents": [
                {
                    "kind": "drive#fileLink",
                    "id": gfolder_id
                }
            ]
        })
        file1.SetContentString(file)
        file1.Upload()  # Upload the file.
        print(file1.GetContentString())

