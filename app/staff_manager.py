import json
import logging
from typing import List
from app.models import Staff

logger = logging.getLogger("api")

class StaffManager:
    def __init__(self):
        self.data_file = "app/data/staff.json"
        self.staff = self._load_staff()

    def _load_staff(self) -> List[dict]:
        """Load staff from JSON file"""
        try:
            with open(self.data_file, "r") as f:
                staff_data = json.load(f)
                logger.info(f"Loaded {len(staff_data)} staff members from file")
                return staff_data
        except FileNotFoundError:
            logger.warning("Staff data file not found, starting with empty list")
            return []
        except json.JSONDecodeError:
            logger.error("Error decoding staff JSON, starting with empty list")
            return []

    def save_data(self):
        """Save staff to JSON file"""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.staff, f, indent=4)
            logger.debug("Staff data saved successfully")
        except Exception as e:
            logger.error(f"Error saving staff data: {e}")
            raise

    def get_all_staff(self) -> List[dict]:
        """Get all staff"""
        return self.staff

    def get_staff(self, staff_id: int) -> dict:
        """Get staff by ID"""
        staff = next((s for s in self.staff if s["id"] == staff_id), None)
        if staff:
            logger.debug(f"Retrieved staff with ID: {staff_id}")
        else:
            logger.debug(f"Staff with ID {staff_id} not found")
        return staff

    def add_staff(self, staff: Staff) -> dict:
        """Add a new staff member"""
        staff_dict = staff.model_dump()
        
        # Check if staff with same ID already exists
        if any(s["id"] == staff_dict["id"] for s in self.staff):
            logger.warning(f"Staff with ID {staff_dict['id']} already exists")
            raise ValueError(f"Staff with ID {staff_dict['id']} already exists")
        
        self.staff.append(staff_dict)
        self.save_data()
        logger.info(f"Added new staff: {staff_dict}")
        return staff_dict

    def update_staff(self, staff_id: int, updated_staff: Staff) -> dict:
        """Update an existing staff member"""
        for i, staff in enumerate(self.staff):
            if staff["id"] == staff_id:
                self.staff[i] = updated_staff.model_dump()
                self.save_data()
                logger.info(f"Updated staff with ID: {staff_id}")
                return self.staff[i]
        
        logger.warning(f"Staff with ID {staff_id} not found for update")
        return None

    def delete_staff(self, staff_id: int):
        """Delete a staff member by ID"""
        initial_count = len(self.staff)
        self.staff = [staff for staff in self.staff if staff["id"] != staff_id]
        
        if len(self.staff) < initial_count:
            self.save_data()
            logger.info(f"Deleted staff with ID: {staff_id}")
        else:
            logger.warning(f"Staff with ID {staff_id} not found for deletion")