from abc import ABC, abstractmethod


class AbstractStore(ABC):

    @abstractmethod
    def store(self, obj):
        pass

    @abstractmethod
    def load(self, query):
        pass

    @abstractmethod
    def delete(self, query):
        pass

    @abstractmethod
    def update(self, message):
        pass
