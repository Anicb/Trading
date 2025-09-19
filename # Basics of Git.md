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

## Navigating Across Codespace, Workspace, and Repository

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