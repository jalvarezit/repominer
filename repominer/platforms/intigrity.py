from repominer.platforms.base import BugBountyPlatformScraper


class IntigrityPlatform(BugBountyPlatformScraper):
    @staticmethod
    def get_provider() -> str:
        return "intigrity"

    @staticmethod
    def get_session_key() -> str:
        return "intigrity_session"
    
    @staticmethod
    def get_pat_key() -> str:
        return "intigrity_pat"

    def process_scopes(self, cb):
        pass
