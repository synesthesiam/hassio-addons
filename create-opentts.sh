#!/usr/bin/env bash
set -e
this_dir="$( cd "$( dirname "$0" )" && pwd )"
base_dir="${this_dir}/opentts-base"

function set_lang_version {
    # lang input output
    sed -e "s/@LANG@/$1/g" -e "s/@VERSION@/$2/g" "$3" > "$4"
}

export -f set_lang_version

version='2.1'
for lang in 'de' 'es' 'en' 'el' 'fi' 'fr' 'hu' 'it' 'ja' 'ko' 'nl' 'ru' 'sv' 'zh'; do
    repo_dir="${this_dir}/opentts-${lang}"
    mkdir -p "${repo_dir}"

    # Copy static files
    cp -f \
       "${base_dir}/run.sh" \
       "${repo_dir}/"

    # Copy dynamic files
    find "${base_dir}" -name '*.in' -type f -print0 | \
        parallel -0 -n1 \
                 set_lang_version "${lang}" "${version}" {} "${repo_dir}/{/.}"

    # Create icon
    composite \
        -geometry +0+17 \
        "${base_dir}/flags/${lang}_small.png" \
        "${base_dir}/icon.png" \
        "${repo_dir}/icon.png"

    # Create logo
    composite \
        -geometry +70+3 \
        "${base_dir}/flags/${lang}_large.png" \
        "${base_dir}/logo.png" \
        "${repo_dir}/logo.png"
done
