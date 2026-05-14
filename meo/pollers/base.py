from abc import ABC, abstractmethod
from typing import List, Dict


class BasePoller(ABC):
    name: str = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        ...

    @abstractmethod
    def poll(self) -> List[Dict]:
        ...

    def safe_poll(self) -> List[Dict]:
        if not self.is_configured():
            return []
        try:
            return self.poll()
        except Exception as e:
            print(f"[{self.name}] poll failed: {e}")
            return []
