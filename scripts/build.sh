#!/usr/bin/env bash

SAVE_IMAGES=false

for arg in "$@"; do
  if [[ "$arg" == "--save-images" ]]; then
    SAVE_IMAGES=true
  fi
done

docker compose -f docker-compose.yml -f docker-compose.dev.yml build

if [ "$SAVE_IMAGES" = true ]; then
  echo "Saving images from docker-compose.yml..."
  IMAGES=$(docker compose -f docker-compose.yml config | awk '/image:/ { print $2 }')

  for IMAGE in $IMAGES; do
    SAFE_NAME=$(echo "$IMAGE" | sed 's/[\/:]/_/g')
    docker save "$IMAGE" | gzip -9 > "${SAFE_NAME}.tar.gz"
    echo "Saved $IMAGE as ${SAFE_NAME}.tar"
  done
fi