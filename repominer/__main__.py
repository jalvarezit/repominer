from argparse import ArgumentParser, SUPPRESS
import logging
from os import getenv
from repominer.platforms.base import BugBountyPlatformFactory
from repominer.platforms.hackerone import HackerOnePlatform
from repominer.platforms.bugcrowd import BugcrowdPlatform
from repominer.platforms.intigrity import IntigrityPlatform
from repominer.vsproviders.base import VersionControlSourceFactory
from repominer.vsproviders.github import GithubSource

def main():
    parser = ArgumentParser(
        prog='repominer',
        description='Tool to extract open source projects from bug bounty scopes'
    )

    # Debug mode
    parser.add_argument('-d', '--debug', action='store_true', help=SUPPRESS)

    parser.add_argument(f'--{BugcrowdPlatform.get_session_key()}', type=str, default=getenv(BugcrowdPlatform.get_session_key().upper()), help='Bugcrowd session')
    parser.add_argument(f'--{IntigrityPlatform.get_session_key()}', type=str, default=getenv(IntigrityPlatform.get_session_key().upper()), help='Intigrity session')
    parser.add_argument(f'--{HackerOnePlatform.get_username_key()}', type=str, default=getenv(HackerOnePlatform.get_username_key().upper()), help='HackerOne username')
    parser.add_argument(f'--{HackerOnePlatform.get_token_key()}', type=str, default=getenv(HackerOnePlatform.get_token_key().upper()), help='HackerOne PAT')

    args = parser.parse_args()
    
    # Set logging level
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    bb_factory = BugBountyPlatformFactory(vars(args))
    vcs_factory = VersionControlSourceFactory()

    for platform in bb_factory.get_platforms():
        platform.process_scopes(vcs_factory.find_svc)

if __name__ == '__main__':
    main()
