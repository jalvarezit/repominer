import logging
from typing import List, TypeVar

import requests
from repominer.platforms.base import BugBountyPlatformScraper
from repominer.vsproviders.base import VersionControlSource


class BugcrowdPlatform(BugBountyPlatformScraper):

    def __init__(self, config: dict) -> None:
        self.session_key = config.get(BugcrowdPlatform.get_session_key())

    @staticmethod
    def get_provider() -> str:
        return "bugcrowd"

    @staticmethod
    def get_session_key() -> str:
        return "bugcrowd_session"

    def process_scopes(self, cb) -> List[VersionControlSource]:
        result = []
        session = requests.session()

        session.cookies.update(
            {"_crowdcontrol_session_key": self.session_key}
        )
        programs_list_url_template = "https://bugcrowd.com/programs.json?sort[]=promoted-desc&page[]={}"
        program_url_template = "https://bugcrowd.com/{}/target_groups"

        page = 1
        # Loop while programs is not empty
        while True:
            resp = session.get(programs_list_url_template.format(page))

            programs = resp.json().get("programs")
            if len(programs) == 0:
                break
            
            # Process each program found
            for program in programs:
                # Remove the first slash
                program_url = program.get("program_url")[1:]
                logging.debug(f"Processing {program_url}")
                if program_url.startswith("programs/teasers"):
                    logging.debug("Skipping teaser program")
                    continue
                program_data_url = program_url_template.format(program_url)
                resp = session.get(program_data_url)
                for svc in cb(resp.json().get('overview')):
                    print(f"{program_data_url}\t{svc}")
                    result += [svc]
            page += 1

        return result
