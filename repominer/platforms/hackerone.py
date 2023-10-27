from typing import List

import requests
from repominer.platforms.base import BugBountyPlatformScraper
from repominer.vsproviders.base import VersionControlSource


class HackerOnePlatform(BugBountyPlatformScraper):

    def __init__(self, config: dict) -> None:
        self.username = config.get(HackerOnePlatform.get_username_key())
        self.token = config.get(HackerOnePlatform.get_token_key())
        
        if not self.username or not self.token:
            raise ValueError("HackerOne username and PAT are required")

    @staticmethod
    def get_provider() -> str:
        return "hackerone"

    '''
    Cookie session not implemented, they use GraphQL not in the mood of
    dealing with that right now
    '''
    @staticmethod
    def get_username_key() -> str:
        return "hackerone_username"
    
    @staticmethod
    def get_token_key() -> str:
        return "hackerone_token"

    def process_scopes(self, cb) -> List[VersionControlSource]:
        result = []
        session = requests.session()

        session.auth = (
            self.username,
            self.token
        )

        program_list_url = 'https://api.hackerone.com/v1/hackers/programs?page[size]=100'
        program_url_template = 'https://hackerone.com/{}'
        structured_scopes_url_template = "https://api.hackerone.com/v1/hackers/programs/{}/structured_scopes"
        
        # TODO: Add an auxiliar function that receives a callback and makes
        # requests until there are no more pages

        while True:
            resp = session.get(program_list_url)

            body = resp.json()
            
            links = body["links"]
            data = body["data"]

            for program in data:
                handle = program["attributes"]["handle"]
                api_url = structured_scopes_url_template.format(handle)

                program_url = program_url_template.format(handle)

                while True:
                    resp = session.get(api_url)
                    body = resp.json()
                    
                    scopes = []

                    for scope in body["data"]:
                        if scope["attributes"]["asset_type"] != "SOURCE_CODE":
                            continue
                        asset_identifier = scope["attributes"]["asset_identifier"]
                        instruction = scope["attributes"]["instruction"]

                        scopes .append(asset_identifier)
                        if instruction:
                            scopes.append(instruction)

                    if "next" in body["links"]:
                        api_url = body["links"]["next"]
                    else:

                        for svc in cb(*scopes):
                            print(f"{program_url}\t{svc}")
                        break

            if "next" in links:
                program_list_url = links["next"]
            else:
                break

        return result
