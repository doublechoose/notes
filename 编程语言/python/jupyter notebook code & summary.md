# jupyter notebook code & summary

### backend: Tornado

python web framework and asynchronous networking library. using non-blocking network I/O.

4 major components:

- web framework
- client and server-side implementations of HTTP
- asynchronous networking library.
- coroutine library





### Notebook and file contents API

| HTTP verb | URL                                                       | Action                                                       |
| --------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| `GET`     | /api/contents                                             | Return a model for the base directory. See /api/contents/\<path>/\<file>. |
| `GET`     | /api/contents /\<file>                                    | Return a model for the given file in the base directory. See /api/contents/\<path>/\<file>. |
| `GET`     | /api/contents /\<path>/\<file>                            | Return a model for a file or directory. A directory model contains a list of models (without content) of the files and directories it contains. |
| `PUT`     | /api/contents /\<path>/\<file>                            | Saves the file in the location specified by name and path. PUT is very similar to POST, but the requester specifies the name, whereas with POST, the server picks the name. PUT /api/contents/path/Name.ipynb Save notebook at `path/Name.ipynb`. Notebook structure is specified in `content` key of JSON request body. If content is not specified, create a new empty notebook. PUT /api/contents/path/Name.ipynb with JSON body::{ "copy_from" : "[path/to/]OtherNotebook.ipynb" } Copy OtherNotebook to Name |
| `PATCH`   | /api/contents /\<path>/\<file>                            | PATCH renames a notebook without re-uploading content.       |
| `POST`    | /api/contents /<path>/<file>                              | Create a new file or directory in the specified path. POST creates new files or directories. The server always decides on the name. POST /api/contents/path New untitled notebook in path. If content specified, upload a notebook, otherwise start empty. POST /api/contents/path with body {"copy_from" : "OtherNotebook.ipynb"} New copy of OtherNotebook in path |
| `DELETE`  | /api/contents /<path>/<file>                              | delete a file in the given path                              |
| `GET`     | /api/contents /<path>/<file> /checkpoints                 | get lists checkpoints for a file.                            |
| `POST`    | /api/contents /<path>/<file> /checkpoints                 | post creates a new checkpoint.                               |
| `POST`    | /api/contents /<path>/<file> /checkpoints/<checkpoint_id> | post restores a file from a checkpoint.                      |
| `DELETE`  | /api/contents /<path>/<file> /checkpoints/<checkpoint_id> | delete clears a checkpoint for a given file.                 |