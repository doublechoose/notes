# jupyterhub 

调整UI

```
python3 setup.py js    # fetch updated client-side js
python3 setup.py css   # recompile CSS from LESS sources
```

### `lessc` not found

If the `python3 -m pip install --editable .` command fails and complains about`lessc` being unavailable, you may need to explicitly install some additional JavaScript dependencies:

```
npm install
```

