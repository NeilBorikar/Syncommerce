from pymongo.database import Database
from app.repositories.base_repository import BaseRepository

class AppointmentRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["appointments"])

    def get_by_business_and_date(self, business_id: str, date: str):
        appointments = self.collection.find({"business_id": business_id, "date": date}).sort("token_number", 1)
        return self._convert_many(list(appointments))

    def get_patient_appointment(self, patient_id: str, date: str):
        app = self.collection.find_one({"patient_id": patient_id, "date": date})
        if app:
            return self._convert_one(app)
        return None
