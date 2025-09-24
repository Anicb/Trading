# Basics of Git

This reference summarizes common Git concepts, commands, and troubleshooting steps discussed in our chat. It includes user doubts and responses for practical understanding.

---

## Key Concepts

- **Remote**: A version of your repository hosted elsewhere (e.g., GitHub). The default remote is usually called `origin`.
- **Ref (Reference)**: A pointer to a commit, such as a branch (`main`), tag, or HEAD.

---

## Git Codespace, Workspace, and Repository

### What is a GitHub Codespace?
- A **Codespace** is a cloud-based development environment provided by GitHub.
- It runs in a container on GitHub’s infrastructure, giving you a ready-to-code setup with your repository cloned.
- You can access it from anywhere, and it includes tools, extensions, and your code.

### What is a Workspace?
- In VS Code and similar editors, a **workspace** is the set of files and folders you are currently working on.
- In Codespaces, your workspace is the environment inside the container, but locally, it refers to the files on your computer.
- You can open, edit, and manage files in your workspace.

### What is a Repository?
- A **repository** (repo) is the version-controlled storage for your code, history, and configuration.
- It can be hosted remotely (e.g., on GitHub) or locally on your machine.
- You interact with the repository using Git commands.

---

### Navigating Across Codespace, Workspace, and Repository

- **Starting Work:**  
  - You create or open a Codespace from your GitHub repository.  
  - This clones the repository into your Codespace workspace.

- **Editing Code:**  
  - You work in your workspace (the set of files in the Codespace or locally).
  - Changes are made to files in the workspace.

- **Saving and Sharing Changes:**  
  - You use Git commands to stage, commit, and push changes from your workspace to the remote repository.
  - Other collaborators can pull these changes into their own workspaces or Codespaces.

- **Resuming Work:**  
  - If your Codespace is deleted, you can create a new one from the repository.
  - Your workspace will be restored with the latest pushed changes.

---

## Common Git Commands

### Checking Status

```bash
git status
```
Shows the current state of your working directory and staging area.

### Viewing Unpushed Commits

```bash
git log --branches --not --remotes
```
Lists commits present locally but not yet pushed to the remote.

### Adding and Committing Changes

```bash
git add .
git commit -m "Your commit message"
```
Stages and commits your changes.

### Pushing Changes

```bash
git push
```
Uploads your local commits to the remote repository.

---

## Troubleshooting

### Push Rejected Due to Remote Updates

**Error:**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/Anicb/Trading'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Solution:**
Pull the latest changes and reapply your commits:
```bash
git pull --rebase
git push
```

---

## Example Workflow

1. **Check status**
    ```bash
    git status
    ```
    Output: `nothing to commit, working tree clean`

2. **Check for unpushed commits**
    ```bash
    git log --branches --not --remotes
    ```
    Output: (nothing)

3. **Add, commit, and push**
    ```bash
    git add .
    git commit -m "commit #2"
    git push
    ```
    If push is rejected, follow the solution above.

4. **Pull with rebase if needed**
    ```bash
    git pull --rebase
    git push
    ```

---

## Common Doubts & Answers

**Q: What is a remote?**  
A: A remote is a version of your repository hosted on a service like GitHub.

**Q: What is a ref?**  
A: A ref is a pointer to a commit, such as a branch or tag.

**Q: Why did my push fail?**  
A: The remote had new commits you didn’t have locally. Pull and rebase, then push again.

**Q: How do I resume work after Codespace deletion?**  
A: As long as you push your changes, you can create a new Codespace from your repository and continue working.

**Q: Why did my commit and push fail with "pathspec 'push' did not match"?**  
A: You entered both commands on one line. Run them separately.

**Q: How do I navigate between Codespace, workspace, and repository?**  
A: Open a Codespace from your repository, work in your workspace, and use Git to sync changes with the repository.

---

## Useful Tips

- Always pull before pushing if you suspect remote changes.
- Use `git status` and `git log` to check your repo state.
- Separate commands when using the terminal.
- Codespaces are cloud workspaces; your repository is the source of truth.

---
## Git management across local and repository while cloning

### Move local code to your actual GitHub repository
Create a new repository on GitHub (if you haven't already).
In your local folder, open a terminal and run:

```bash
git init # to initialize git in local repo
git remote set-url origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
#### main vs master

If your local branch is called master, replace main with master.

When you push your code to GitHub, you need to specify the branch name. Most new repositories use main as the default branch, but older ones may use master.

(check with ```git branch```).


#### If you cloned from a different repo

You need to run 'git remote remove origin' first, then 'git remote add origin ...'
i.e.
If you cloned from a different repository, your local repo’s remote (origin) points to the original source. You need to update it to your own GitHub repository.

To check current remote:
```git remote -v```

Would give the following output:
origin  https://github.com/jamwithai/arxiv-paper-curator (fetch)
origin  https://github.com/jamwithai/arxiv-paper-curator (push)

To change it:

Remove the old remote: ```git remote remove origin```

Add your own GitHub repo as remote:
```git remote add origin https://github.com/your-username/your-repo.git```

Push your branch:
```git push -u origin main   # or master, depending on your branch name```

#### Troubleshooting Git Errors when pushing local cloned repository to a new GitHub repository, understanding "remote" and "origin".

---

What are "remote" and "origin"?

- **Remote**: In Git, a remote is a version of your project hosted elsewhere (usually on GitHub, GitLab, etc.).
- **origin**: This is the default name Git gives to the main remote repository you cloned from or push to. You can have multiple remotes, but `origin` is the standard for the primary one.

---

##### Common Error: Push Rejected after removing Origin and adding Origin to your repo

When you try to push your local branch to GitHub, you may see:

```
! [rejected] main -> main (fetch first)
error: failed to push some refs to 'https://github.com/Anicb/Jam'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Reason:**  
The remote repository already has commits that your local repo does not. Git prevents you from overwriting those changes.

---

##### Step-by-Step Resolution

###### 1. Set Your Git Identity

Git needs your name and email for commit history.

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

###### 2. Set Branch Tracking

If your local branch is not tracking the remote branch, set it:

```bash
git branch --set-upstream-to=origin/main main
```

###### 3. Pull Remote Changes

Fetch and merge any changes from the remote repository:

```bash
git pull
```

If you see merge conflicts, resolve them in your code editor, then continue.

###### 4. Add and Commit Your Changes

Stage and commit your changes:

```bash
git add .
git commit -m "moving local to git repo"
```

###### 5. Push to Your GitHub Repository

Push your local branch to the remote repository:

```bash
git push
```

##### Error when Git Pull fails after setting branch tracking 

The error fatal: refusing to merge unrelated histories occurs when your local repository and the remote repository have completely separate commit histories (e.g., both were initialized independently).

###### How to Fix
You can force Git to merge unrelated histories by adding the --allow-unrelated-histories flag:

``` git pull origin main --allow-unrelated-histories ```

This will merge the remote and local histories.
You may be prompted to resolve merge conflicts (especially if both repos have files with the same name, like README.md or .env). Then resolve conflicts, commit, and push.
---

Notes

- Always pull remote changes before pushing to avoid overwriting others' work.
- If you see merge conflicts, resolve them before committing and pushing.
- Setting your Git identity is required for all commits.

---

### Clone directly into your GitHub repository
You cannot "clone" directly into a new GitHub repository. Cloning always creates a local copy. To copy code from one repo to another on GitHub, you can:

Fork the original repo on GitHub (creates a copy under your account).
Or, use GitHub's "Import repository" feature.

### Codespaces: Is it better?
Using GitHub Codespaces lets you work in a cloud-based dev environment directly linked to your GitHub repo.
You can clone, push, and manage code without local setup.
It's ideal for collaborative or cloud-based workflows, but not strictly necessary for simple local-to-GitHub transfers.