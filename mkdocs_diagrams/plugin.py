import concurrent.futures
import logging
import os
import shutil
import subprocess
import sys
import time

import mkdocs
import mkdocs.plugins

from mkdocs.structure.files import get_files

# This global is a hack to keep track of the last time the plugin rendered diagrams.
# A global is required because plugins are reinitialized each time a change is detected.
last_run_timestamp = 0


class DiagramsPlugin(mkdocs.plugins.BasePlugin):
    """
    A MkDocs plugin to render Diagrams files.

    See also https://diagrams.mingrammer.com/.
    """

    config_scheme = (
        (
            "file_extension",
            mkdocs.config.config_options.Type(str, default=".diagrams.py"),
        ),
        ("max_workers", mkdocs.config.config_options.Type(int, default=None)),
    )

    def __init__(self):
        self.log = logging.getLogger("mkdocs.plugins.diagrams")
        self.pool = None

    def _create_threadpool(self):
        max_workers = self.config["max_workers"]
        if max_workers is None:
            max_workers = os.cpu_count() + 2
        self.log.debug(
            "Using up to %d concurrent workers for diagrams rendering", max_workers
        )
        return concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    def _render_diagram(self, file):
        self.log.debug(f"Rendering {file.name}")
        # The two commented lines below would build in the destination
        # (site_dir) directory instead of the original source directory.
        # Unfortunately this results in incorrect image URLs (they don't get
        # rewritten to the proper relative path one directory up).
        #
        # dest_dir = os.path.dirname(file.abs_dest_path)
        # filename = file.abs_dest_path[len(dest_dir)+1:]
        dest_dir = os.path.dirname(file.abs_src_path)
        filename = file.abs_src_path[len(dest_dir) + 1:]

        # Even when writing in abs_src_path rather than abs_dest_path, this
        # seems needed to make livereload accurately pick up changes.
        os.makedirs(os.path.dirname(file.abs_dest_path), exist_ok=True)
        shutil.copy(file.abs_src_path, file.abs_dest_path)

        # Try to get the full path to the currently used interpreter. This
        # helps ensure we use the right one even with virtualenvs, etc.,
        # especially on Windows.
        # (See https://github.com/zoni/mkdocs-diagrams/issues/2)
        python_path = sys.executable

        # If Python is unable to retrieve the real path to its
        # executable, sys.executable will be an empty string or None.
        if python_path is None or python_path == "":
            python_path = "python"

        subprocess.run([python_path, filename], check=True, cwd=dest_dir)

    def _walk_files_and_render(self, config):
        pool = self._create_threadpool()
        files = get_files(config)
        jobs = []
        for file in files:
            if file.src_path.endswith(self.config["file_extension"]):
                jobs.append(pool.submit(self._render_diagram, file))

        for job in concurrent.futures.as_completed(jobs):
            try:
                job.result()
            except Exception:
                self.log.exception("Worker raised an exception while rendering a diagram")

    def on_pre_build(self, config):
        global last_run_timestamp
        if int(time.time()) - last_run_timestamp < 10:
            self.log.info(
                "Watcher started looping, skipping diagrams rendering on this run"
            )
            return
        self._walk_files_and_render(config)
        last_run_timestamp = int(time.time())
