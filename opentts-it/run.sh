#!/usr/bin/env bash

PYTHON=/app/usr/local/bin/python3

function jq {
    "${PYTHON}" -c 'import sys; import json; print(json.load(open(sys.argv[2]))[sys.argv[1]])' "$@"
}

export -f jq

OPENTTS_ARGS=()

if [[ -f "${CONFIG_PATH}" ]]; then
    # Hass.IO configuration

    # Directory to cache WAV files (use /tmp if no argument)
    cache_dir="$(jq 'cache_dir' "${CONFIG_PATH}")"
    if [[ -n "${cache_dir}" ]]; then
        OPENTTS_ARGS+=('--cache' "${cache_dir}")
    fi

    # If true, print DEBUG messages to log
    debug="$(jq 'debug' "${CONFIG_PATH}")"
    if [[ "${debug}" == 'True' ]]; then
        OPENTTS_ARGS+=('--debug')
    fi

    # Larynx-specific settings
    larynx_quality="$(jq 'larynx_quality' "${CONFIG_PATH}")"
    if [[ -n "${larynx_quality}" ]]; then
        OPENTTS_ARGS+=('--larynx-quality' "${larynx_quality}")
    fi

    larynx_noise_scale="$(jq 'larynx_noise_scale' "${CONFIG_PATH}")"
    if [[ -n "${larynx_noise_scale}" ]]; then
        OPENTTS_ARGS+=('--larynx-noise-scale' "${larynx_noise_scale}")
    fi

    larynx_length_scale="$(jq 'larynx_length_scale' "${CONFIG_PATH}")"
    if [[ -n "${larynx_length_scale}" ]]; then
        OPENTTS_ARGS+=('--larynx-length-scale' "${larynx_length_scale}")
    fi

    echo "${OPENTTS_ARGS[@]}"
fi

cd /app

if [[ -z "${OPENTTS_ARGS[*]}" ]]; then
    "${PYTHON}" app.py "$@"
else
    "${PYTHON}" app.py "${OPENTTS_ARGS[@]}" "$@"
fi
