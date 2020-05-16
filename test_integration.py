import shutil
import subprocess
import os

MKDOCS_CONFIG = """
site_name: mkdocs-diagrams
docs_dir: docs

plugins:
  - diagrams
"""


def file_contents(path):
    with open(path, 'r') as f:
        return f.read()


def test_build(tmp_path):
    with open(tmp_path / "mkdocs.yml", "w") as f:
        f.write(MKDOCS_CONFIG)
    shutil.copytree("test_docs", tmp_path / "docs")
    shutil.copy("README.md", tmp_path / "docs" / "README.md")

    subprocess.run(
        ["mkdocs", "build", "--verbose", "--strict", "--site-dir", tmp_path / "site"],
        check=True,
        cwd=tmp_path
    )

    index_html = file_contents(tmp_path / "site" / "index.html")
    assert "mkdocs-diagrams" in index_html
    assert os.path.exists(tmp_path / "site" / "event_processing.png")
