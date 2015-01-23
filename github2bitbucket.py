#!/usr/bin/env python
#-*- coding: utf-8 -*-

# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the bitbucket issue migration script.
# If not, see <http://www.gnu.org/licenses/>.

import itertools
import json
import zipfile
import argparse
import urllib2
import os
from getpass import getpass
from github3 import login, GitHubError

def read_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "A tool to migrate a whole repo from Github to Bitbucket.\n"
            "Works for public and private repos.\n"
            "Migrates source, wiki and issues."
        )
    )

    parser.add_argument(
        "-p", "--passphrases",
        help="Are you using ssh passphrases?",
	action = "store_true"
    )

    parser.add_argument(
        "bitbucketUsername",
        help="Your Bitbucket username"
    )

    parser.add_argument(
        "bitbucketRepo",
        help="Bitbucket repo to migrate to. Format: <username>/<repo name>"
    )

    parser.add_argument(
        "githubUsername",
        help="Your GitHub username"
    )

    parser.add_argument(
        "githubRepo",
        help="GitHub repo to migrate from. Format: <username>/<repo name>"
    )
    return parser.parse_args()

def exportIssues(githubUsername, githubPassword, githubRepoUser, githubRepoName):
  try:
      gh = login(githubUsername, githubPassword)
  except GitHubError:
      parser.exit(1, "Invalid credentials.\n")

  repo = gh.repository(githubRepoUser, githubRepoName)
  if not repo:
      parser.exit(1, "Invalid repository.\n")

  meta = {
      'default_kind': 'bug'
  }
  issues = []
  comments = []
  milestones = []

  for issue in itertools.chain(repo.iter_issues(), repo.iter_issues(state='all')):
      issues.append({
	  'id': issue.id,
	  'created_on': issue.created_at.isoformat(),
	  'updated_on': issue.updated_at.isoformat(),
	  'content_updated_on': issue.updated_at.isoformat(),
	  'assignee': issue.assignee.login if issue.assignee else None,
	  'reporter': issue.user.login,
	  'milestone': issue.milestone.title if issue.milestone else None,
	  'title': issue.title,
	  'content': issue.body,
	  'status': 'resolved' if issue.is_closed() else 'open',
	  'kind': 'bug', # todo: determine based on labels
	  'priority': 'minor' # todo: determine based on labels
      })

      if issue.comments > 0:
	  for comment in issue.iter_comments():
	      comments.append({
		  'id': comment.id,
		  'content': comment.body,
		  'created_on': comment.created_at.isoformat(),
		  'updated_on': comment.updated_at.isoformat(),
		  'issue': issue.number,
		  'user': comment.user.login
	      })

  for milestone in repo.iter_milestones():
      milestones.append({'name': milestone.title})

  output = {
      'meta': meta,
      'issues': issues,
      'comments': comments,
      'milestones': milestones
  }

  with zipfile.ZipFile(repo.name + 'IssuesForBitbucket.zip', 'w') as z:
      z.writestr('db-1.0.json', json.dumps(output))

if __name__ == "__main__":
  options = read_arguments()
  if not args.passphrases:
    print "Github password for {}".format(options.githubUsername)
    githubPassword = getpass()
    print "Bitbucket password for {}".format(options.bitbucketUsername)
    bitbucketPassword = getpass()
    bitbucketUrl = "https://{0}:{1}@bitbucket.org/{2}".format(options.bitbucketUsername, bitbucketPassword, options.bitbucketRepo)
    githubUrl = "https://{0}:{1}@github.com/{2}".format(options.githubUsername, githubPassword, options.githubRepo)
    githubWikiRepoUrl = "https://{0}:{1}@github.com/{2}.wiki.git".format(options.githubUsername, githubPassword, options.githubRepo)
    bitbucketWikiRepoUrl = "https://{0}:{1}@bitbucket.org/{2}/wiki".format(options.bitbucketUsername, bitbucketPassword, options.bitbucketRepo)
  else:
    bitbucketUrl = "https://bitbucket.org/{}".format(options.bitbucketRepo)
    githubUrl = "https://github.com/{}".format(options.githubRepo)
    githubWikiRepoUrl = "https://github.com/{}.wiki.git".format(options.githubRepo)
    bitbucketWikiRepoUrl = "https://bitbucket.org/{}/wiki".format(options.bitbucketRepo)
  os.system("git pull")
  os.system("git push --mirror {}".format(bitbucketUrl))
  os.system("git remote set-url origin {}".format(bitbucketUrl))
  os.system("mkdir git2bitbucketWikiTemp")
  os.system("cd git2bitbucketWikiTemp")
  print "Migrated repo source"
  os.system("git clone {}".format(githubWikiRepoUrl))
  os.chdir("{}.wiki".format(options.githubRepo.split("/")[1]))
  os.system("git push --mirror {}".format(bitbucketWikiRepoUrl))
  os.system("git remote set-url origin {}".format(bitbucketWikiRepoUrl))
  print "Migrated repo wiki"
  exportIssues(options.githubUsername, githubPassword, options.githubRepo.split("/")[0], options.githubRepo.split("/")[1])