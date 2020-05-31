#!/usr/bin/env bash

if [[ -f "${CONFIG_PATH}" ]]; then
    # Hass.IO configuration
    profile_name="$(jq --raw-output '.profile_name' "${CONFIG_PATH}")"
    profile_dir="$(jq --raw-output '.profile_dir' "${CONFIG_PATH}")"
    RHASSPY_ARGS=('--profile' "${profile_name}" '--user-profiles' "${profile_dir}")

    # Copy user-defined asoundrc to root
    asoundrc="$(jq --raw-output '.asoundrc' "${CONFIG_PATH}")"
    if [[ ! -z "${asoundrc}" ]]; then
	    echo "${asoundrc}" > /root/.asoundrc
    fi

    # Add SSL settings
    ssl="$(jq --raw-output '.ssl' "${CONFIG_PATH}")"
    if [[ "${ssl}" == 'true' ]]; then
        certfile="$(jq --raw-output '.certfile' "${CONFIG_PATH}")"
        keyfile="$(jq --raw-output '.keyfile' "${CONFIG_PATH}")"
        RHASSPY_ARGS+=('--ssl' "/ssl/${certfile}" "/ssl/${keyfile}")
    fi
fi

if [[ -z "${RHASSPY_ARGS[*]}" ]]; then
    /usr/bin/rhasspy "$@"
else
    /usr/bin/rhasspy "${RHASSPY_ARGS[@]}" "$@"
fi
