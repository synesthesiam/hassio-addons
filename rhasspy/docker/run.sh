#!/usr/bin/env bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
RHASSPY_APP=/usr/share/rhasspy
RHASSPY_USER_DIR=/share/rhasspy
RHASSPY_PROFILE=en
RHASSPY_EXTRA_ARGS=""

if [[ -f "${CONFIG_PATH}" ]]; then
    RHASSPY_USER_DIR="$(jq --raw-output '.user_dir' ${CONFIG_PATH})"
    RHASSPY_PROFILE="$(jq --raw-output '.profile' ${CONFIG_PATH})"
    RHASSPY_SSL="$(jq --raw-output '.ssl' ${CONFIG_PATH})"
    if [[ "${RHASSPY_SSL}" = "true" ]]; then
        RHASSPY_CERTFILE="$(jq --raw-output '.certfile' ${CONFIG_PATH})"
        RHASSPY_KEYFILE="$(jq --raw-output '.keyfile' ${CONFIG_PATH})"
        RHASSPY_EXTRA_ARGS="${RHASSPY_EXTRA_ARGS} --ssl ${RHASSPY_CERTFILE} ${RHASSPY_KEYFILE}"
    fi
fi

mkdir -p "${RHASSPY_USER_DIR}"

cd "${RHASSPY_APP}"
python3 app.py \
    --user-profiles "${RHASSPY_USER_DIR}" \
    --profile "${RHASSPY_PROFILE}" \
    "${RHASSPY_EXTRA_ARGS}" \
    "$@"
