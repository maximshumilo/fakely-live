#!/usr/bin/env bash

set -e

# Find project version in config file.
function get_project_version() {
  local SEARCH_TEMPLATE="^version = .*$"
  project_version=$(grep -E "$SEARCH_TEMPLATE" pyproject.toml | awk '{print $3}')

  # Remove quote character ("1.0.0" -> 1.0.0).
  project_version=${project_version//\"}
  echo "$project_version"
}
get_project_version
