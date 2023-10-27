from abc import ABC, abstractmethod
import importlib
import inspect
import logging
import re
from typing import TypeVar, List

T = TypeVar('T', bound='VersionControlSource')


class VersionControlSource(ABC):

    def __init__(self, source: str) -> None:
        if not source.strip():
            raise ValueError("Source cannot be empty")
        self._source = source

    @property
    def source(self) -> str:
        return self._source

    @property
    @staticmethod
    @abstractmethod
    def get_provider() -> str:
        raise NotImplementedError

    @property
    @staticmethod
    @abstractmethod
    def get_technology() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_regex() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_debug_regex() -> str:
        raise NotImplementedError

    @staticmethod
    def _hydrate_regex(regex: str) -> re.Pattern:
        hydrated = r'(?<=[\\\\s\[\(])?' + regex + r'(?=[\s\]\\\)]?)'
        return re.compile(hydrated)
    
    @staticmethod
    def _add_scheme(url: str) -> str:
        if not url.startswith("http"):
            return "https://" + url
        return url

    @classmethod
    def find_sources(cls: T, *data: str, debug: bool = False) -> List[T]:
        regex = cls.get_regex()
        logging.debug(f"Searching for {cls.get_provider()} sources using regex {regex}")
        matches = []
        for d in data:
            matches += re.findall(regex, d)
        unique_matches = list(set(matches))
        logging.debug(f"Found {len(unique_matches)} matches")
        if debug:
            debug_matches = []
            for d in data:
                debug_matches += re.findall(cls.get_debug_regex(), d)
            debug_unique_matches = list(set(debug_matches))
            if len(debug_unique_matches) != len(unique_matches):
                logging.debug(f'Found different amount of matches in debug mode')
                logging.debug(f'Scope: {data}')
        return [cls(match) for match in unique_matches]

    def __repr__(self) -> str:
        return f"{self.get_technology()}\t{self.get_provider()}\t{self._add_scheme(self.source)}"

class VersionControlSourceFactory():

    def __init__(self, debug: bool = False) -> None:
        self.classes: List[T] = self._get_all_vcs()
        self.debug = debug
    def _get_all_vcs(self) -> List[T]:
        vcs_list = []
        # Remember that if they don't fully implement the abstract class
        # it won't load them but it won't fail either
        module = importlib.import_module(__package__)
        for name, obj in inspect.getmembers(module):
            # Check that is alphanumeric to avoid importing modules starting with underscore
            if inspect.ismodule(obj) and name.isalnum():
                for name, obj in inspect.getmembers(obj):
                    if inspect.isclass(obj) and issubclass(obj, VersionControlSource) and obj != VersionControlSource:
                        logging.debug(f"Loaded version countrol source {obj}")
                        vcs_list.append(obj)
        return vcs_list
        
    def find_svc(self, *data: str) -> List[T]:
        svc_list = []
        for vcs in self.classes:
            svc_list += vcs.find_sources(*data, debug=self.debug)
        return svc_list
