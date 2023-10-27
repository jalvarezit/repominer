from typing import List, TypeVar
from repominer.vsproviders.base import VersionControlSource

T = TypeVar('T', bound='GitlabSource')

class GitlabSource(VersionControlSource):

    @classmethod
    def get_regex(cls) -> str:
        return cls._hydrate_regex(r'(https?://)?gitlab\.com\/\w+\/?\w+\/?\*?')
    
    @staticmethod
    def get_provider() -> str:
        return "gitlab"
    