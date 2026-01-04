#!/usr/bin/env python3
"""Track items with status"""

import json
import time
from typing import List, Dict, Optional
from pathlib import Path


class Item:
    """Represents a trackable item"""
    
    def __init__(self, text: str):
        self.id = str(int(time.time() * 1000))
        self.text = text
        self.state = "new"
        self.created = time.time()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "text": self.text,
            "state": self.state,
            "created": self.created
        }


class Tracker:
    """Main tracking system"""
    
    def __init__(self, path: Optional[str] = None):
        self.items: Dict[str, Item] = {}
        self.path = Path(path) if path else None
        if self.path and self.path.exists():
            self._load()
    
    def add(self, text: str) -> Item:
        item = Item(text)
        self.items[item.id] = item
        return item
    
    def get(self, item_id: str) -> Optional[Item]:
        return self.items.get(item_id)
    
    def set_state(self, item_id: str, state: str) -> bool:
        item = self.get(item_id)
        if item:
            item.state = state
            return True
        return False
    
    def list_active(self) -> List[Item]:
        return [i for i in self.items.values() if i.state == "active"]
    
    def save(self) -> bool:
        if not self.path:
            return False
        try:
            data = {
                "items": [i.to_dict() for i in self.items.values()],
                "saved": time.time()
            }
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(data, indent=2))
            return True
        except Exception:
            return False
    
    def _load(self) -> bool:
        if not self.path or not self.path.exists():
            return False
        try:
            data = json.loads(self.path.read_text())
            for d in data.get("items", []):
                item = Item(d["text"])
                item.id = d["id"]
                item.state = d["state"]
                item.created = d["created"]
                self.items[item.id] = item
            return True
        except Exception:
            return False


if __name__ == "__main__":
    t = Tracker()
    a = t.add("Test item one")
    b = t.add("Test item two")
    t.set_state(a.id, "active")
    print(f"Items: {len(t.items)}")
    print(f"Active: {len(t.list_active())}")
