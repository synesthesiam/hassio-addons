#!/usr/bin/env bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
RHASSPY_APP=/usr/share/rhasspy
RHASSPY_USER_DIR=/share/rhasspy
RHASSPY_PROFILE=en

if [[ -f "${CONFIG_PATH}" ]]; then
    RHASSPY_USER_DIR="$(jq --raw-output '.user_dir' ${CONFIG_PATH})"
    RHASSPY_PROFILE="$(jq --raw-output '.profile' ${CONFIG_PATH})"

    asoundrc="$(jq --raw-output '.asoundrc' ${CONFIG_PATH})"
    if [[ ! -z "${asoundrc}" ]]; then
        echo "${asoundrc}" > /root/.asoundrc
    fi
fi

mkdir -p "${RHASSPY_USER_DIR}"

cd "${RHASSPY_APP}"
python3 app.py \
    --user-profiles "${RHASSPY_USER_DIR}" \
    --profile "${RHASSPY_PROFILE}" \
    "$@"
