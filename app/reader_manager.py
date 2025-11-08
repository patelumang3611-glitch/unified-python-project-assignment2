import json
import logging
from typing import List
from app.models import Reader

logger = logging.getLogger("api")

class ReaderManager:
    def __init__(self):
        self.data_file = "app/data/readers.json"
        self.readers = self._load_readers()

    def _load_readers(self) -> List[dict]:
        """Load readers from JSON file"""
        try:
            with open(self.data_file, "r") as f:
                readers_data = json.load(f)
                logger.info(f"Loaded {len(readers_data)} readers from file")
                return readers_data
        except FileNotFoundError:
            logger.warning("Readers data file not found, starting with empty list")
            return []
        except json.JSONDecodeError:
            logger.error("Error decoding readers JSON, starting with empty list")
            return []

    def save_data(self):
        """Save readers to JSON file"""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.readers, f, indent=4)
            logger.debug("Readers data saved successfully")
        except Exception as e:
            logger.error(f"Error saving readers data: {e}")
            raise

    def get_all_readers(self) -> List[dict]:
        """Get all readers"""
        return self.readers

    def get_reader(self, reader_id: int) -> dict:
        """Get reader by ID"""
        reader = next((r for r in self.readers if r["id"] == reader_id), None)
        if reader:
            logger.debug(f"Retrieved reader with ID: {reader_id}")
        else:
            logger.debug(f"Reader with ID {reader_id} not found")
        return reader

    def add_reader(self, reader: Reader) -> dict:
        """Add a new reader"""
        reader_dict = reader.model_dump()
        
        # Check if reader with same ID already exists
        if any(r["id"] == reader_dict["id"] for r in self.readers):
            logger.warning(f"Reader with ID {reader_dict['id']} already exists")
            raise ValueError(f"Reader with ID {reader_dict['id']} already exists")
        
        self.readers.append(reader_dict)
        self.save_data()
        logger.info(f"Added new reader: {reader_dict}")
        return reader_dict

    def update_reader(self, reader_id: int, updated_reader: Reader) -> dict:
        """Update an existing reader"""
        for i, reader in enumerate(self.readers):
            if reader["id"] == reader_id:
                self.readers[i] = updated_reader.model_dump()
                self.save_data()
                logger.info(f"Updated reader with ID: {reader_id}")
                return self.readers[i]
        
        logger.warning(f"Reader with ID {reader_id} not found for update")
        return None

    def delete_reader(self, reader_id: int):
        """Delete a reader by ID"""
        initial_count = len(self.readers)
        self.readers = [reader for reader in self.readers if reader["id"] != reader_id]
        
        if len(self.readers) < initial_count:
            self.save_data()
            logger.info(f"Deleted reader with ID: {reader_id}")
        else:
            logger.warning(f"Reader with ID {reader_id} not found for deletion")