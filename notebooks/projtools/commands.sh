#!/bin/bash

pyproj() {
    if ! check-valid-environment; then
        return 1
    fi

    if [ "$1" == "install" ] && [ "$2" == "environment" ]; then
        if [ -z "$4" ]; then
            echo "Name for environment not given."
            return 1
        fi
        conda env create -f "$PROJTOOLS_PROJECT_PATH/environment.yml" -n "$4"
        conda activate "$4"
        pip install -U -r "$PROJTOOLS_PROJECT_PATH/requirements.txt"
    elif [ "$1" == "update" ] && [ "$2" == "environment" ]; then
        conda env update -f "$PROJTOOLS_PROJECT_PATH/environment.yml"
        pip install -U -r "$PROJTOOLS_PROJECT_PATH/requirements.txt"
    elif [ "$1" == "reinstall" ] && [ "$2" == "environment" ]; then
        if [ -z "$4" ]; then
            echo "Name for environment not given."
            return 1
        fi
        conda env remove -n "$4"
        pyproj install environment -n "$4"
    elif [ "$1" == "setup" ] && [ "$2" == "xeus-python" ]; then
        echo "y" | jupyter kernelspec uninstall python3
        conda install -y xeus-python notebook -c conda-forge
    elif [ "$1" == "generate" ] && [ "$2" == "requirements" ]; then
        cp "$PROJTOOLS_PROJECT_PATH/projtools/environment.yml" "$PROJTOOLS_PROJECT_PATH"
        cp "$PROJTOOLS_PROJECT_PATH/projtools/requirements.txt" "$PROJTOOLS_PROJECT_PATH"
    else
        echo "Invalid arguments"
        return 1
    fi
}

projtools() {
    if [ "$1" == "init" ]; then
        if check-current-directory; then
            export PROJTOOLS_PROJECT_PATH=$PWD
        else
            echo "projtools folder not found in working directory. projtools should be initialized in a directory that contains the projtools folder."
            return 1
        fi
    fi
}

check-valid-environment() {
    if [ -z "$PROJTOOLS_PROJECT_PATH" ]; then
        if ! check-current-directory; then
            echo "Invalid working directory. Commands must either be run from a directory containing the projtools folder or you must run projtools init from that directory."
            return 1
        fi

        projtools init
    fi

}

check-current-directory() {
    if ! test -d "$PWD/projtools"; then
        return 1
    fi
}

# ken-probe() {
#     if [ $1 == "init" ]; then
#         if test -f "$PWD/environment.yml"; then
#             export KENPROBE_PROJECT_PATH=$PWD
#         else
#             echo "This is not the root directory of the project. You must run ken-probe init from the root directory of the project."
#         fi
#     elif [ -z "$KENPROBE_PROJECT_PATH" ]; then
#         echo "Project not initialized. You must run ken-probe init from the root directory of the project."
#     else
#         case $1 in
#             install)
#                 conda env create -f "$KENPROBE_PROJECT_PATH/environment.yml" --prefix "$KENPROBE_PROJECT_PATH/envs"
#                 ken-probe activate environment
#                 pip install -U -r "$KENPROBE_PROJECT_PATH/requirements.txt"
#                 ;;
#             activate)
#                 conda activate "$KENPROBE_PROJECT_PATH/envs"
#                 ;;
#             deactivate)
#                 conda deactivate
#                 ;;
#             update)
#                 conda env "export" > "$KENPROBE_PROJECT_PATH/environment.yml" --from-history
#                 ;;
#         esac
#     fi
# }
