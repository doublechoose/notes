conda 入门



```
conda --version

conda update conda
```

Create a new environment and install a package in it.

We will name the environment `snowflakes` and install the package BioPython. At the Anaconda Prompt or in your Terminal window, type the following:

```
conda create --name snowflakes biopython
```

Verify that the snakes environment has been added and is active:

```
conda info --envs
```

Conda displays the list of all environments with an asterisk (*) after the name of the active environment:

```
# conda environments:
#
base                     /home/username/anaconda3
snakes                *  /home/username/anaconda3/envs/snakes
snowflakes               /home/username/anaconda3/envs/snowflakes
```

1. To find a package you have already installed, first activate the environment you want to search. Look above for the commands to [activate your snakes environment](https://conda.io/docs/user-guide/getting-started.html#managing-envs).

2. Check to see if a package you have not installed named “beautifulsoup4” is available from the Anaconda repository (must be connected to the Internet):

   ```
   conda search beautifulsoup4
   ```

