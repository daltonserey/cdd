function cdt {
    echo 'ok 2'
}

function cd {
    if [[ $# == 0 ]]; then
        # no argument used
        command cd
        return 0
    fi

    if [[ $# == 1 ]] && [[ -d "$1" ]]; then
        # argument is a directory in current directory
        command cd "$1"

        # add directory to the database
        ~/cdd/cdd -a $PWD

        # and that's all
        return 0
    fi

    # assume argument $1 is a pattern
    cddmatch=$(~/cdd/cdd $1 | head -1)
    if [[ -d "$cddmatch" ]]; then
        command cd $cddmatch
    else
        ~/cdd/cdd -d "$cddmatch"
    fi
}
