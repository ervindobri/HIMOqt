import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from helpers.constants import RESOURCES_PATH


class FirestoreDatabase:
    def __init__(self):
        cred = credentials.Certificate(RESOURCES_PATH + "himo-cd380-firebase-adminsdk-mkum9-a259734f0b.json")
        firebase_admin.initialize_app(cred, {
            'projectId': 'himo-cd380',
        })

        db = firestore.client()

        self.patients = db.collection(u'patients')

    def set_patient_data(self, patient, emg):
        print("EMG size:", emg)
        data = {
            u'id': patient.id,
            u'age': patient.age,
            u'emg': emg
        }
        self.patients.document(u'LA').set(data)
