#!/bin/bash

# Load the .env file
set -a
source ./.env
set +a

# Default values for parameters
build_target="both"
tag="latest"

# Function to display help
function show_help() {
    echo "Usage: ./script.sh [options]"
    echo ""
    echo "Options:"
    echo "  --d [app, db]      Specify the target to build:"
    echo "                     - 'app' builds only the API image (from Dockerfile.api)"
    echo "                     - 'db' builds only the DB image (from Dockerfile.db)"
    echo "                     - If omitted, both images will be built"
    echo ""
    echo "  --t [latest, dev]  Specify the tag for the Docker image version:"
    echo "                     - 'latest' (default) sets the image tag to :latest"
    echo "                     - 'dev' sets the image tag to :dev"
    echo ""
    echo "  --help             Show this help message and exit"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --d)
            build_target="$2"
            shift 2
            ;;
        --t)
            tag="$2"
            shift 2
            ;;
        --help)
            show_help
            ;;
        *)
            echo "Unknown parameter: $1"
            show_help
            ;;
    esac
done

# Login to Docker
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# Determine which images to build based on the parameters
if [[ "$build_target" == "both" || "$build_target" == "app" ]]; then
    echo "Building API Image with tag :$tag"
    docker build -t ghcr.io/$GITHUB_PACKAGE:$tag -f Dockerfile.api .
    echo "Pushing API Image with tag :$tag"
    docker push ghcr.io/$GITHUB_PACKAGE:$tag
fi

if [[ "$build_target" == "both" || "$build_target" == "db" ]]; then
    echo "Building DB Image with tag :$tag"
    docker build -t ghcr.io/$GITHUB_PACKAGE_REPO/$GITHUB_PACKAGE_DB:$tag -f Dockerfile.db .
    echo "Pushing DB Image with tag :$tag"
    docker push ghcr.io/$GITHUB_PACKAGE_REPO/$GITHUB_PACKAGE_DB:$tag
fi
