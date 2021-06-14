import json

from helpers.uploader import GDriveUploader

if __name__ == '__main__':
    uploader = GDriveUploader()
    content = {
        'id': 99,
        'age': 99,
        'emg': [9900]
    }
    uploader.upload('9999.json', json.dumps(content, allow_nan=True))