projtools() {
    if [ $1 == "init" ]; then
        if test -f "$PWD/environment.yml"; then
            export PROJTOOLS_PROJECT_PATH=$PWD
        else
            echo "This is not the root directory of the project. You must run projtools init from the root directory of the project."
        fi
    elif [ -z "$PROJTOOLS_PROJECT_PATH" ]; then
        echo "Project not initialized. You must run projtools init from the root directory of the project."
    else
        case $1 in
            install)
                conda env create -f "$PROJTOOLS_PROJECT_PATH/environment.yml" --prefix "$PROJTOOLS_PROJECT_PATH/envs"
                projtools activate environment
                projtools pip-install
                ;;
            pip-install)
                pip install -U -r "$PROJTOOLS_PROJECT_PATH/requirements.txt"
                rm -r "$PROJTOOLS_PROJECT_PATH/backend/notebooks"
                cp -r "$PROJTOOLS_PROJECT_PATH/notebooks/notebooks" "$PROJTOOLS_PROJECT_PATH/backend/notebooks"
              ;;
            install-pip)
              projtools pip-install
              ;;
            activate)
                conda activate "$PROJTOOLS_PROJECT_PATH/envs"
                ;;
            deactivate)
                conda deactivate
                ;;
            update)
                conda env "export" > "$PROJTOOLS_PROJECT_PATH/environment.yml" --from-history
                ;;
        esac
    fi
}
