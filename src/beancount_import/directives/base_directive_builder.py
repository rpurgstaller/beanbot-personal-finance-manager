from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from model.transaction import DbTransaction


class BaseDirectiveBuilder(ABC):

    @property
    @abstractmethod
    def directives(self) -> None:
        pass

    @abstractmethod
    def build_directives(self, db_transaction : DbTransaction):
        pass

    