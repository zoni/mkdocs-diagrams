# mkdocs-diagrams

A plugin for the [MkDocs] documentation site generator which facilitates easy embedding of system architecture diagrams through the [Diagrams] project.

## Installation

`mkdocs-diagrams` is available on PyPI.
It can be installed through `pip install mkdocs-diagrams` or equivalent command with pipenv or poetry.

Once installed, configure MkDocs to use it by including `diagrams` in the `plugins` list in your `mkdocs.yml`.
For example:

```yaml
plugins:
  - diagrams
  - search
```

(If you don't have a `plugins` key in your config yet, you'll almost surely want to include `search` as well.
It's a default plugin that will otherwise get deactivated.)

## Usage

> **Warning:** This plugin will execute `.diagram.py` files during build, as that is how [Diagrams] itself operates.
> Be careful using this plugin with untrusted input as this effectively allows arbitrary code execution.

Once installed, the diagrams plugin can be used by including diagrams files in your docs directory.

For example, create a file named `example.diagrams.py` with the following contents:

```python
from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3


with Diagram("Event Processing", show=False):
    source = EKS("k8s source")

    with Cluster("Event Flows"):
        with Cluster("Event Workers"):
            workers = [ECS("worker1"),
                       ECS("worker2"),
                       ECS("worker3")]

        queue = SQS("event queue")

        with Cluster("Processing"):
            handlers = [Lambda("proc1"),
                        Lambda("proc2"),
                        Lambda("proc3")]

    store = S3("events store")
    dw = Redshift("analytics")

    source >> workers >> queue >> handlers
    handlers >> store
    handlers >> dw
```

When MkDocs is run (either with `build` or `serve`), this will result in a file named `event_processing.png` being created.
Include this in your markdown files using regular image syntax: `![Event processing architecture](event_processing.png)`

## Configuration

This plugin supports a few config options, which can be set as follows:

```yaml
plugins:
  - diagrams:
      file_extension: ".diagrams.py"
      max_workers: 5
```

### `file_extension`

Sets the filename extension for diagram files.
When `mkdocs build` or `mkdocs serve` is run, all files ending in this extension will be executed.

Default: `.diagrams.py`

### `max_workers`

A pool of workers is used to render diagram files in parallel on multi-core systems.
Setting this allows you to limit the number of workers to this amount.

Default: Dynamically chosen (`os.cpu_count() + 2`)

[diagrams]: https://diagrams.mingrammer.com/
[mkdocs]: https://www.mkdocs.org/
