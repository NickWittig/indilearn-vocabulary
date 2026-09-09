from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass
