import subprocess
import requests
from itertools import dropwhile, takewhile
from os import environ

with open(".jazzy.yaml") as file:
    data = file.readlines()
for line in data:
    if line.startswith("module_version: "):
        version = line[len("module_version: "):]

print("WARNING: If you continue, this script will run the standard git commands.\nOnce this script has been tested, you can remove this confirm check.\n")
input("Input anything to continue, or use Ctrl-C to stop the script")

subprocess.run("git checkout master")
subprocess.run("git pull")
desc = input("Input a description of this release ")
subprocess.run(f'git tag -s v{version} -m "Version {version}: {desc}"')
subprocess.run("git push --tags")
subprocess.run("git checkout development")
subprocess.run("git pull")
subprocess.run("git rebase master")
subprocess.run("git push")

with open("CHANGELOG") as file:
    changelog = "\n".join(list(takewhile(lambda x: not x.startswith("## "), list(dropwhile(lambda x: not x.startswith("## "), file.readLines()))[3:])))

print("WARNING: If you continue, this script will ruse the GitHub API to make a release.\nOnce this script has been tested, you can remove this confirm check.\n")
input("Input anything to continue, or use Ctrl-C to stop the script")

url = "https://api.github.com/repos/Samasaur1/DiceKit/releases"
json = {
  "tag_name": f"v{version}",
  "target_commitish": "master",
  "name": f"Version {version}: {desc}",
  "body": f"""{changelog}

[See changelog](https://github.com/Samasaur1/DiceKit/blob/master/CHANGELOG.md)
[See docs](https://samasaur1.github.io/DiceKit/)
""",
  "draft": True, #This could be changed to False if this script works
  "prerelease": version.startswith("0.")
}
headers = {'Authorization': f'token {environ.get("GH_TOKEN")}'}
response = requests.post(url, json=json, headers=headers)
if response.ok:
    print("API call successful")
else:
    print(f"API call unsuccessful — status code {response.status_code}")

print("A release was created, but as a draft — you need to publish it at https://github.com/Samasaur1/DiceKit/releases")