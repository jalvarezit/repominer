import re
from typing import List, TypeVar
from repominer.vsproviders.base import VersionControlSource

T = TypeVar('T', bound='GithubSource')

class GithubSource(VersionControlSource):

    @classmethod
    def get_regex(cls) -> re.Pattern:
        return cls._hydrate_regex(r'github\.com/\w+(?:/\w+)?')

    @classmethod
    def get_debug_regex(cls) -> re.Pattern:
        return re.compile(r'github\.com/')

    @staticmethod
    def get_provider() -> str:
        return "github"
    
    @staticmethod
    def get_technology() -> str:
        return "git"    
