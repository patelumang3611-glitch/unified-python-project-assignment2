import json
from typing import List
from app.models import Staff

DATA_FILE = "data/staff_data.json"

class StaffManager:
    def __init__(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.staff = json.load(f)
        except FileNotFoundError:
            self.staff = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.staff, f, indent=4)

    def get_all_staff(self) -> List[Staff]:
        return self.staff

    def get_staff(self, staff_id: int):
        return next((s for s in self.staff if s["id"] == staff_id), None)

    def add_staff(self, staff: Staff):
        self.staff.append(staff.model_dump())
        self.save_data()
        return staff

    def update_staff(self, staff_id: int, updated_staff: Staff):
        for i, s in enumerate(self.staff):
            if s["id"] == staff_id:
                self.staff[i] = updated_staff.model_dump()
                self.save_data()
                return updated_staff
        return None

    def delete_staff(self, staff_id: int):
        self.staff = [s for s in self.staff if s["id"] != staff_id]
        self.save_data()
