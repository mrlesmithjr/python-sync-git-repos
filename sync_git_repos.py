#!/usr/bin/env python
"""
A simple script to scan a path for git directories to abstract info and sync.
"""

import argparse
import os
import json
import git
from git import Repo
import gitdb


def get_args():
    """Get CLI command arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to scan', required=True)
    parser.add_argument('-o', '--outfile', help='Save JSON results to file.')
    args = parser.parse_args()

    if args.path.endswith('/'):
        args.path = args.path.rstrip('/')

    return args


def main(arguments):
    """Main program execution."""
    repos = dict()
    # scan repos_DIR for directories
    for directory in os.scandir(arguments.path):
        if directory.is_dir():
            # Define directory full path
            path = directory.path
            # Ensure that directory is a git repo
            if os.path.isdir(os.path.join(path, '.git')):
                repo = Repo(path)
                # Obtain repo name from last portion of the path. This may not
                # always match repo_url, but should work for our use case here.
                repo_name = path.split('/')[-1]

                # Define initial repo name within the repos dictionary
                repos[repo_name] = dict()

                # Add full path to repo directory
                repos[repo_name]['path'] = path

                # Define currently active branch within git repo
                active_branch = repo.active_branch
                repos[repo_name]['active_branch'] = active_branch.name

                # Iterate over git remotes and abstract remote info
                repos[repo_name]['remotes'] = []
                try:
                    for remote in repo.remotes:
                        for fetch_info in remote.fetch():
                            if fetch_info.flags == 4:
                                remote_changes = False
                            else:
                                remote_changes = True
                                if active_branch.name == 'master':
                                    remote.pull(rebase=True)
                            remote_info = {'name': remote.name,
                                           'ref': fetch_info.ref.name,
                                           'url': remote.url,
                                           'remote_changes': remote_changes}
                            repos[repo_name]['remotes'].append(remote_info)
                except git.exc.GitCommandError:
                    pass

                # Iterate over any git submodules found and abstract some info
                repos[repo_name]['submodules'] = []
                try:
                    submodules = repo.submodules
                    for submodule in submodules:
                        submodule_info = {
                            'name': submodule.name, 'url': submodule.url}
                        repos[repo_name]['submodules'].append(submodule_info)
                except gitdb.exc.BadName:
                    pass

                repos[repo_name]['changed_files'] = []

                # Obtain whether or not the repo is in a dirty state or not.
                dirty = repo.is_dirty()
                repos[repo_name]['dirty'] = dirty
                if dirty:
                    changed_files = repo.index.diff(None)
                    for changed_file in changed_files:
                        repos[repo_name]['changed_files'].append(
                            changed_file.a_path)

                # Capture any untracked files in the git repo directory
                untracked_files = repo.untracked_files
                repos[repo_name]['untracked_files'] = untracked_files

                # Capture any git tags and iterate over them
                repos[repo_name]['tags'] = []
                for tag in repo.tags:
                    repos[repo_name]['tags'].append(tag.name)

    return repos


if __name__ == "__main__":
    ARGS = get_args()
    REPOS = main(ARGS)
    if ARGS.outfile is None:
        print(json.dumps(REPOS, indent=4))
    else:
        with open(ARGS.outfile, 'w') as stream:
            json.dump(REPOS, stream, indent=4)
            stream.close()
