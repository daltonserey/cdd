# cdd

cdd is a set of scripts written in python and bash that make it
easier to navigate file system directories. It allows the user to
jump directly to frequently used directories, typing just a
few characters contained in the directory basename.

## installation

*Step 1: install `cdd`*. Use `pip install --user cdd`. I didn't
test whether it works installed as root user. Alternatively, you
can download the files directly from GitHub.

*Step 2: set up paths*. Once the scripts are installed, make
sure your `PATH` and your `PYTHONPATH` include `cdd` directories.
Usually, `pip --user` installs scripts in `~/.local/bin`. In this
case, set your `PATH` to include that directory. And the library
will be installed under `~/.local/lib/python2.7`. In this case,
set your `PYTHONPATH` to include that directory.

*Step 3: set up the `cd` function*. This is achieved by sourcing
the `cdd-bash-function.sh` file. You can test `cdd` without
making it permanent, by sourcing the file containing the `cd`
function issuing the command `source
~/.local/bin/cdd-bash-function.sh`. To make it permanent, source
the file from within your `~/.profile`.

## use

Simply use `cd` as you are used to. Whenever you use `cd` to
navigate in the usual way within the file system, `cdd` will
store the directories seen. Once the directory is in the cdd
database, you can navigate directly to that directory, by typing

> `cd <pattern>`

where `<pattern>` is any part of the name of the subdirectory.
