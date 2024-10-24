### Read the Docs

:::{note}
Adapted from <https://cookiecutter-hypermodern-python.readthedocs.io/en/2022.6.3.post1/guide.html#read-the-docs>
:::

[Read the Docs] automates the building, versioning, and hosting of documentation.

Follow these steps to set up Read the Docs for your repository:

1. Sign up at [Read the Docs].
2. Import your GitHub repository,
   using the button _Import a Project_.
3. Install the GitHub [webhook][readthedocs webhooks],
   using the button _Add integration_
   on the _Integrations_ tab
   in the _Admin_ section of your project
   on Read the Docs.

Read the Docs automatically starts building your documentation,
and will continue to do so when you push to the default branch or make a release.
Your documentation now has a public URL like this:

> `https://<project>.readthedocs.io/`

The configuration for Read the Docs is included in the repository,
in the file [.readthedocs.yml][readthedocs.yaml].

Build dependencies for the documentation
are installed using the pyproject.toml file, with the `doc` extra dependencies.

[read the docs]: https://readthedocs.org/
[readthedocs.yaml]: https://docs.readthedocs.io/en/stable/config-file/v2.html#configuration-file-v2
[readthedocs webhooks]: https://docs.readthedocs.io/en/stable/webhooks.html
