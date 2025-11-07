import json
from typing import List
from app.models import Reader

DATA_FILE = "data/readers_data.json"

class ReaderManager:
    def __init__(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.readers = json.load(f)
        except FileNotFoundError:
            self.readers = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.readers, f, indent=4)

    def get_all_readers(self) -> List[Reader]:
        return self.readers

    def get_reader(self, reader_id: int):
        return next((r for r in self.readers if r["id"] == reader_id), None)

    def add_reader(self, reader: Reader):
        self.readers.append(reader.model_dump())
        self.save_data()
        return reader

    def update_reader(self, reader_id: int, updated_reader: Reader):
        for i, r in enumerate(self.readers):
            if r["id"] == reader_id:
                self.readers[i] = updated_reader.model_dump()
                self.save_data()
                return updated_reader
        return None

    def delete_reader(self, reader_id: int):
        self.readers = [r for r in self.readers if r["id"] != reader_id]
        self.save_data()
