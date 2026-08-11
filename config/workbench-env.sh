# Export approved workbench settings from the ignored environment file.
# The loader reads the file line by line and never executes its content.
# Only the allowlisted keys below are exported.
# Usage: . config/workbench-env.sh [path-to-workbench.env]
workbench_env_file="${1:-config/workbench.env}"
if [ -f "$workbench_env_file" ]; then
  while IFS= read -r workbench_line || [ -n "$workbench_line" ]; do
    case "$workbench_line" in
      AIMAAS_BASE_URL=* | AIMAAS_MODEL_ID=* | AIMAAS_API_KEY=* | \
      AIMAAS_API_KEY_HEADER=*)
        export "${workbench_line%%=*}=${workbench_line#*=}"
        ;;
    esac
  done <"$workbench_env_file"
fi
unset workbench_env_file workbench_line
