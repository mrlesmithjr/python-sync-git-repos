# python-sync-git-repos

## Purpose

Provides the ability to pass a path to where your directories are located which
contain your git repos that you maintain. All directories are scanned and checked
for an existing `.git` subdirectory. If found, the git information is abstracted
from, the directory into JSON format and printed to stdout. At the same time,
a git fetch is performed within the directory to check for changes upstream. If
changes are found, and the active branch is master, a git pull rebase is performed.
If you maintain hundreds of git repositories as I do, this provides many benefits
and they are not limited to the functionality that is implemented.

## Requirements

- Python3

```bash
pip3 install -r requirements.txt
```

## Usage

### Display Help

```bash
python sync_git_repos.py --help
...
usage: sync_git_repos.py [-h] -p PATH [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to scan
  -o OUTFILE, --outfile OUTFILE
                        Save JSON results to file.
```

### Execution

#### Display to stdout

```bash
python sync_git_repos.py --path ~/Git_Projects/Personal/GitHub/mrlesmithjr
```

##### Example Results

```json
{
  "ansible-offline-yum-repo": {
    "path": "/Users/larrysmithjr/Git_Projects/Personal/GitHub/mrlesmithjr/ansible-offline-yum-repo",
    "active_branch": "master",
    "remotes": [
      {
        "name": "origin",
        "ref": "origin/master",
        "url": "git@github.com:mrlesmithjr/ansible-offline-yum-repo.git",
        "remote_changes": false
      }
    ],
    "submodules": [],
    "changed_files": [],
    "dirty": false,
    "untracked_files": [],
    "tags": []
  },
  "ansible-policy-based-routing": {
    "path": "/Users/larrysmithjr/Git_Projects/Personal/GitHub/mrlesmithjr/ansible-policy-based-routing",
    "active_branch": "master",
    "remotes": [
      {
        "name": "origin",
        "ref": "origin/master",
        "url": "git@github.com:mrlesmithjr/ansible-policy-based-routing.git",
        "remote_changes": false
      }
    ],
    "submodules": [],
    "changed_files": [],
    "dirty": false,
    "untracked_files": [],
    "tags": []
  }
}
```

#### Save to JSON file

```bash
python sync_git_repos.py --path ~/Git_Projects/Personal/GitHub/mrlesmithjr --outfile repos.json
```

## License

MIT

## Author Info

Larry Smith Jr.

- [@mrlesmithjr](https://twitter.com/mrlesmithjr)
- [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
- [mrlesmithjr@gmail.com](mailto:mrlesmithjr@gmail.com)
