# Contributing Guide

Thank you for your contribution in helping us improve the documentation for Percona Server for MongoDB!

We welcome contributors from all users and the community. By contributing, you agree to the [Percona Community code of conduct](https://github.com/percona/community/blob/main/content/contribute/coc.md).

You can contribute to documentation in the following ways:

## Rate and comment on documentation pages

Each documentation page includes a **Rate this page** feature that allows you to assign stars (1-5) and leave comments. This is a quick and easy way to provide feedback about the documentation.

To rate a page:

1. Use the star rating system to rate the page (1-5 stars).

2. Leave a comment describing your feedback.

>[!Important]
Help us improve the documentation faster by leaving clear and detailed comments. This helps us understand the issue and address it more efficiently.

Brief comments like “this is confusing” or “needs improvement” are helpful, but sharing a bit more context allows us to take the most appropriate action.

Please include:
* What issue did you encounter, or what improvement would you like to see
* Which section or topic needs clarification or correction
* Any specific examples or use cases that would help
* The version or environment you're using (if relevant)
* Steps to reproduce any issues you found

## Add a topic in the Percona Community Forum

The [Percona Community Forum](https://forums.percona.com/) is a public discussion platform where you can ask questions, share feedback, or suggest improvements to the documentation. Use the forum to start a conversation about documentation issues, request clarifications, or discuss potential changes with the community and documentation team.

To add a topic, navigate to the [Percona Product Documentation category](https://forums.percona.com/c/percona-product-documentation/71) in the Percona Community Forum and select **New Topic**. Complete the form and select **Create Topic** to add the topic to the forum.

## Request a change with a Jira issue

Create a Jira ticket to report documentation issues or request changes. This method is useful for formal tracking or when you want the documentation team to handle the changes.

1. Sign in (or create a Percona Jira account if you don't have one).

2. Click the **Create** button.

3. Fill in the required fields:

	* **Summary**: Provide a brief description of the issue.

	* **Description**: Provide more information about the issue. If needed, add a Steps To Reproduce section and information about your environment (version number, your operating system, etc.). Be detailed.

	* **Version**, **Environment**, and other relevant fields as needed.

4. Click [Create](https://jira.percona.com/secure/CreateIssue!default.jspa) and then select the **PSMDB** project to submit the ticket.


## Contribute to documentation yourself

Percona Distribution for MongoDB documentation is written in [Markdown](https://www.markdownguide.org/basic-syntax/) language, so you can 
[edit it online via GitHub](#edit-documentation-online-vi-github). If you wish to have more control over the doc process, jump to how to [edit documentation locally](#edit-documentation-locally). 

To contribute to the documentation, you should be familiar with the following technologies:

- [MkDocs](https://www.mkdocs.org/getting-started/) documentation generator. We use it to convert source ``.md`` files to .html and PDF documents.
- [git](https://git-scm.com/) and [GitHub](https://guides.github.com/activities/hello-world/)

There are several active versions of the documentation. Each version has a branch in the repository named accordingly:

- 3.6 (EOL)
- 4.0 (EOL)
- 4.2 (EOL)
- 4.4 (EOL)
- 5.0 (EOL)
- 6.0
- 7.0
- 8.0

The .md files are in the ``docs`` directory. 

### Edit documentation online via GitHub

1. Click the **Edit this page** link on the sidebar. The source ``.md`` file of the page opens in GitHub editor in your browser. If you haven't worked with the repository before, GitHub creates a [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) of it for you.

2. Edit the page. You can check your changes on the **Preview** tab.

3. Commit your changes.

	 - In the *Commit changes* section, describe your changes.
	 - Select the **Create a new branch for this commit and start a pull request** option
	 - Click **Propose changes**.

4. GitHub creates a branch and a commit for your changes. It loads a new page on which you can open a pull request to Percona. The page shows the base branch - the one you offer your changes for, your commit message, and a diff - a visual representation of your changes against the original page.  This allows you to make a last-minute review. When you are ready, click the **Create pull request** button.
5. Someone from our team reviews the pull request and if everything is correct, merges it into the documentation. Then it gets published on the site.

### Edit documentation locally

This option is for users who prefer to work from their computer and/or have full control over the documentation process.

The steps are the following:

1. Fork this repository
2. Clone the repository on your machine:

```sh
git clone git@github.com:<your_name>/psmdb-docs.git
```

3. Change the directory to ``psmdb-docs`` and add the remote upstream repository:

```sh
git remote add upstream git@github.com:percona/psmdb-docs.git
```

4. Pull the latest changes from upstream

```sh
git fetch upstream
git merge upstream/<branch>
```

Make sure that your local branch and the branch you merge changes from are the same. So if you are on ``8.0`` branch, merge changes from ``upstream/8.0``.

5. Create a separate branch for your changes

```sh
git checkout -b <my_changes>
```

6. Make changes
7. Commit your changes
8. Open a pull request to Percona

### Building the documentation

To verify how your changes look, generate the static site with the documentation. This process is called *building*. You can do it in these ways:
You can do it in these ways:

#### Install MkDocs and build locally

To avoid interrupting your running workflows, it's recommended to install MkDocs in a virtual environment.

1. Install [pip](https://pip.pypa.io/en/stable/installing/)
2. Install [MkDocs](https://www.mkdocs.org/getting-started/#installation).
3. Install all required dependencies:
   
```sh
pip install -r requirements.txt
```

4. While in the root directory of the doc project, run the following command to build the documentation:

```sh
mkdocs build 
```

5. Go to the ``site`` directory and open the ``index.html`` file in your web browser to see the documentation.
6. To automatically rebuild the documentation and reload the browser as you make changes, run the following command:

```sh
mkdocs serve 
```

7. To build the PDF documentation, open the `site/print_page.html` in your browser. Save it as PDF. Depending on the browser, you may need to select the Export to PDF, Print - Save as PDF, or just Save and select PDF as the output format.
