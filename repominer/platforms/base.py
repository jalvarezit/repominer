from abc import ABC, abstractmethod
import importlib
import inspect
import logging
from typing import List, TypeVar, Optional, Callable

from repominer.vsproviders.base import VersionControlSource

BBPS = TypeVar('BBPS', bound='BugBountyPlatformScraper')
VSC = TypeVar('VSC', bound='VersionControlSource')

class BugBountyPlatformScraper(ABC):
    def __init__(self, config: dict) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_provider() -> str:
        raise NotImplementedError
    
    @abstractmethod
    def process_scopes(self, cb: Callable[[str], List[VSC]]) -> List[VSC]:
        '''
        This method should a list of results of all scope processed by callback function
        '''
        raise NotImplementedError
    
class BugBountyPlatformFactory():
    def __init__(self, config) -> None:
        self.config = config

    def get_platforms(self) -> Optional[BBPS]:
        platforms = []
        module = importlib.import_module(__package__)
        for name, obj in inspect.getmembers(module):
            # Check that is alphanumeric to avoid importing modules starting with underscore
            if inspect.ismodule(obj) and name.isalnum():
                for name, obj in inspect.getmembers(obj):
                    if inspect.isclass(obj) and issubclass(obj, BugBountyPlatformScraper) and obj != BugBountyPlatformScraper:
                        logging.debug(f"Loaded platform {obj}")
                        platforms.append(obj(self.config))
        return platforms if platforms else None
