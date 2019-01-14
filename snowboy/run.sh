#!/usr/bin/env bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
CONFIG_PATH="/data/options.json"

host="$(jq --raw-output '.host' $CONFIG_PATH)"
port="$(jq --raw-output '.port' $CONFIG_PATH)"
username="$(jq --raw-output '.username' $CONFIG_PATH)"
password="$(jq --raw-output '.password' $CONFIG_PATH)"
reconnect="$(jq --raw-output '.reconnect' $CONFIG_PATH)"
site_id="$(jq --raw-output '.site_id' $CONFIG_PATH)"
wakeword_id="$(jq --raw-output '.wakeword_id' $CONFIG_PATH)"
model="$(jq --raw-output '.model' $CONFIG_PATH)"
sensitivity="$(jq --raw-output '.sensitivity' $CONFIG_PATH)"
audio_gain="$(jq --raw-output '.audio_gain' $CONFIG_PATH)"

cd "$DIR"
FLASK_APP=app.py flask run --host=0.0.0.0 --port=12102 &
python3 main.py \
        --host "$host" \
        --port "$port" \
        --username "$username" \
        --password "$password" \
        --reconnect "$reconnect" \
        --site-id "$site_id" \
        --wakeword-id "$wakeword_id" \
        --model "$model" \
        --sensitivity "$sensitivity" \
        --gain "$audio_gain"
