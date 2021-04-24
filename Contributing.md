#
<p align="center">
  <img src="./static/images/dark-logo.1c6c40e2.png" width="20%">
  <h1 align="center">
    Contributing to MUMBLE API
  </h1>
</p>

A big welcome to Mumble ! 
<br />
Thank you for considering contributing to Mumble !
<br />
It’s because of people like you that open source projects emerge ! 

Reading and following these guidelines will help us make the contribution process easy.

> ⚠ Those who want to contribute on the repo, please refer to the [README.md](https://github.com/divanov11/mumbleapi/blob/master/README.md) and read the [Code Of Conduct](https://github.com/divanov11/mumbleapi/blob/master/Contributing.md) for more informations.

#

### Table of contents

- Contributing to Mumble

      - Code of Conduct
      - Getting Started
      - Issues
      - Pull Requests

- NB  

      - Minor Updates and Pull Requests
      - Getting Help

#

### Code of Conduct

We take our open source community seriously.
<br />
So by participating and contributing to this project, you agree to our [Code of Conduct](https://github.com/divanov11/mumbleapi/blob/master/CodeOfConduct.md).

#

### Getting Started

Contributions are made to this repo via Issues and Pull Requests (PRs).
<br />
<br/>
To contribute :

- Search for **existing Issues and PRs before creating your own**.
- Describe your changes & issues very well by **following our PR & issues templates !**

#

### Issues

Issues are used to report problems with the library, request a new feature, or to discuss potential changes before a PR is created.

If you find an Issue that addresses the problem you're having, please complete this issue with comments.
<br />
You can send screenshots or explain the bug... 

#

### Pull Requests

PRs are always welcome !
<br />
<br />
In general, PRs should:

- Only fix/add the functionality in question **OR** address wide-spread whitespace/style issues, not both.
- **Add unit or integration tests for fixed or changed functionality** (if a test suite already exists).
- Address a single concern in the least number of **changed lines as possible**.
- **Be accompanied by a complete Pull Request template (loaded automatically when a PR is created)**.

#

### NB

In general, we follow the **fork-and-pull**
<br />


#### Steps :

**1. Fork the repository to your own Github account**

**2. Clone the forked project to your machine**

   ```bash
    git clone https://github.com/<your-github-username>/mumbleapi.git
   ```

**3.Add Upstream or the remote of the original project to your local repository**

   ```bash
   # check remotes
   git remote -v
   git remote add upstream https://github.com/divanov11/mumbleapi.git
   ```

**4. Make sure you update the local repository**

   ```bash
   # Get updates
   git fetch upstream
   # switch to master branch
   git checkout master
   # Merge updates to local repository
   git merge upstream/master
   # Push to github repository
   git push origin master
   ```

**5. Create a branch locally with a succinct but descriptive name**

   ```bash
   git checkout -b branch-name
   ```

**6. Commit changes to the branch**

   ```bash
   # Stage changes for commit i.e add all modified files to commit
   git add .
   # You can also add specific files using
   # git add <filename1> <filename2>
   git commit -m "your commit message goes here"
   # check status
   git status
   ```

**7.Following any formatting and testing guidelines specific to this repository**

**8. Push changes to your fork**

   ```bash
   git push origin branch-name
   ```

**9.Open a PR in our repository and follow the PR template so that we can efficiently review the changes.**

**10. After the pull request was merged, fetch the upstream and update the default branch of your fork**

#

### Getting Help

Join us in **[the Discord Server]("https://discord.gg/TxgpyK8pzf")** and post your question there in the correct category with a descriptive tag.

#
