# Changelog

## v1.0.0

- Use `sys.executable` when spawning python subprocesses.
    - This is primarily a bugfix for Windows users, though other Operating Systems could also benefit.
    - Special thanks to [Leonardo Monteiro](https://github.com/decastromonteiro) for helping pinpoint this issue.
- With this plugin now being used successfully in a number of different environments, the version is bumped to 1.0 for a better stability promise.

## v0.0.2

- `diagrams` added as a package dependency.
- Improved error handling. Errors running diagram files are now logged as errors through MkDocs logging handlers.

## v0.0.1

- Initial release.
