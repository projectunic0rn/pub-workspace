from abc import ABC, abstractmethod

# TODO: Have each app implement AppContract
class AppContract(ABC):
    @abstractmethod
    def process_message_posted_event(self):
        pass
