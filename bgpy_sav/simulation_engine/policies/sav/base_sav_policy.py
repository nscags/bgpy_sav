from abc import ABC, abstractmethod


class BaseSAVPolicy(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @abstractmethod
    def validate(self):
        raise NotImplementedError