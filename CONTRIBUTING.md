# Git Cheatsheet

You can install git from https://git-scm.com/ . I recommend having a CLI version of git handy even if you have git in your IDE, just in case something goes wrong. Your IDE should have equivalents of all of these commands.

## General Commands

Note that remote repository refers to the version of the repository that is on github and available for all of us to see, whereas local repository refers to your version of the repository.

* `git clone <repository-url>` will clone the repository into the current directory.
* `git status` will display the current status of the repository, including what changes are being tracked and your current relationship with the remote repository. Use this command to frequently to see what changes you've made.
* `git branch <branch_name>` will create a new branch named `<branch_name>`, use branches when you want to make big changes that entail a pull request, or to get around merge conflicts that you don't know how to resolve.
* `git checkout <branch_name>` will switch your current branch to `<branch_name>`, you may need to commit your changes on the current branch first.
* `git checkout -b <branch_name>` will both create a new branch named `<branch_name>` and then switch to that branch.
* `git log` will display the commit history for your current branch.
* `git add -A` will stage all of your current changes to be committed.
* `git commit -m "<your message>"` will make a commit with all the staged changes and the message `<your message>`.
* `git pull` will get all of other people's changes from the remote repository. If you receive an error about needing to specify the pull strategy, I recommend using merge (rebase false).
* `git push` will push your committed changes to the remote repository. If you are on a fresh branch you may have to use the following command.
* `git push -u origin <branch_name>` will push the changes from your branch onto the remote repository's branch given by `<branch_name>`. Your branch and the remote branch should have the same name.

## Making a Commit

Your basic workflow should consist of branching out if necessary at the start of your work period and then making commits for each of your significant changes. You can rewind your version of the repository to a previous commit if something goes wrong, so I recommend making a commit every time you produce a piece of working code. Once you are finished working on your branch, you should `git pull` to get everyone else's changes, fix any merge conflicts, and then `git push`. Always pull before you push!



The basic steps to making a change and then committing it are:

1. If this is your first time working on the repository, use `git clone https://github.com/grchristensen/avpd.git` in a location where you want to store the repository. You can then navigate into the repository and start making changes.
2. Switch to a new branch if you are about to make big changes that need to be reviewed with another team member. See [Branching Out](#Branching Out)
3. Make your changes to the code base.
4. When you are about ready to commit, do `git status` to check on the repository.
   * Make sure that you ignore any files that shouldn't be committed. See [Ignoring Files](#Ignoring Files)

4. Use `git add -A` to stage all your current changes to be committed.
5. Use `git commit -m "Informative message"` to make the commit.
6. When you're done, do `git pull` if you're on a branch that is on the remote repository.
7. Fix any merge conflicts, see https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts . If you don't know how you should fix the merge conflicts, branch out and push to a new branch on the remote, so that another team member can review the conflicts with you.
8. Do `git push` to get your changes onto the remote repository. If you are on a fresh branch, you will need to use `git push -u origin <branch_name>`, where `<branch_name>` is the name of your current branch.

## Branching Out

Branches allow you to isolate big changes from the rest of the changes made by other team members. If you make a branch and push it onto the remote, we can use Github's pull request feature to easily see all the changes made by the branch before we merge it. Also, if you're having trouble pushing your changes onto the remote repository, you can branch out into a clean branch where there's no possibility for conflicts.

Use the `git branch` and `git checkout` commands from [General Commands](#General Commands) to manage branches.

## Ignoring Files

Please try to avoid committing any files that don't belong on the repository. Examples of files to not include in your commits are: auto generated files from tests/program execution, cache files, and libraries (project dependencies should be recorded in `requirements.txt` and `package.json` files, while the actual library code is downloaded the first time a team member runs `pip install` or `npm install`). Committing files that are auto-generated could cause problems for other team members if their code is generated in an incompatible way that causes merge conflicts.

To keep a file or directory from being committed, you put the name of that file/directory in a `.gitignore` file. There are two main places for `.gitignore` files:

1. In the project root `avpd/`.
2. In each of the sub-project roots, `avpd/notebooks/`, `avpd/backend/`, and `avpd/frontend/`. You should mainly be adding to the `.gitignore` of whatever sub-project  you're working on.

The filenames in `.gitignore` are relative to where the `.gitignore` file is located. For example, if I want to ignore `avpd/notebooks/venv/` using the `avpd/notebooks/.gitignore` file, I should add `venv/` to `avpd/notebooks/.gitignore`.