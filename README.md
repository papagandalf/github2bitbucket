# github2bitbucket

Migrate from a github repo to a bitbucket repo.
The script migrates the source, the wiki and the issues of a github repo to a bitbucket repo.

##Usage
* place the github2bitbucket.py in your github's repo directory (where you work)
* usage: github2bitbucket.py [-h] [-p]
                            bitbucketUsername bitbucketRepo githubUsername githubRepo
  * use the -p parameter if you use ssh passphrases. If not, you will be prompted for your bitbucket and github passwords.
  * bitbucketRepo and githubRepo shoul be in the owner/name format.
* the source and the wiki are uploaded through the script. in the end, you will have in the directory a zip file with your repo's name. Use that to import the issues in the bitbucket [repo](https://confluence.atlassian.com/display/BITBUCKET/Export+or+import+issue+data).

Thanks to [maxcutler](https://github.com/maxcutler/github-issues-to-bitbucket-converter) for the idea on parsing the issue data.
