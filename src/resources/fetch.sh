#!/usr/bin/env bash

version=$1
dir=$2

version=${version:-"0.5.3-rc.2"}
dir=${dir:-"."}

gh="https://github.com/spark/firmware/releases/download/v${version}"

platforms="6 8 10"

platform[6]="photon"
platform[8]="p1"
platform[10]="electron"

parts[6]="1 2"
parts[8]="1 2"
parts[10]="1 2"

# $1 the release to fetch
function fetchRelease
{
    for p in $platforms; do
        name=${platform[$p]}
        parts=${parts[$p]}
        echo "Fetching platform $name (id: $p, parts: $parts)"
        pushd $name
	rm *
        for part in $parts; do
            wget $gh/system-part$part-$version-$name.bin
            echo "fetching url $url"
        done
        popd
    done
}

fetchRelease
