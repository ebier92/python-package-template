"""Runs a series of git commands to merge development into main without triggering a release
by including "[skip release]" in the merge commit message. Useful for merging things that don't
need to trigger a new build and published release such as updates to docs, tests, or CI/CD jobs.
"""

import subprocess

print(
    "You are about to merge the development branch into main. "
    "No release tag will be made and no package will be published. "
    "Do you want to continue? (y/n):"
)
prompt = ""

while prompt.lower() not in ("y", "n"):
    prompt = input()

    if prompt not in ("y", "n"):
        print("Please enter 'y' or 'n' to make a selection.")

if prompt == "n":
    print("Merge process cancelled.")
    exit()

git_commands = (
    "git checkout main",
    "git pull",
    'git merge development --no-ff -m "Merging development into main. [skip release]"',
    "git push",
    "git checkout development",
    "git pull",
    "git merge main",
    "git push",
)

for command in git_commands:
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    if process.returncode != 0:
        raise RuntimeError(
            f"ERROR: Git command '{command}' failed to execute successfully."
        )
