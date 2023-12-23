#!/bin/sh

sed -i "s/version: [0-9]*\.[0-9]*\.[0-9]*/version: ${1}/g" test/integration/default/inspec.yml FORMULA
