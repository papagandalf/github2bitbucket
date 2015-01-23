# github2bitbucket

Migrate from a github repo to a bitbucket repo.
The script migrates the source, the wiki and the issues of a github repo to a bitbucket repo.

##Usage
usage: github2bitbucket.py [-h] [-p]
                            bitbucketUsername bitbucketRepo githubUsername githubRepo
* use the -p parameter if you use ssh passphrases. If not, you will be prompted for your bitbucket and github passwords.
* bitbucketRepo and githubRepo shoul be in the owner/name format.
