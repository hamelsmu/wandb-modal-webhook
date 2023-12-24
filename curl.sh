#!/bin/bash

# Default URL
URL="http://localhost:8000/"

# Check if a URL is provided as the first argument
if [ "$1" != "" ]; then
    URL=$1
fi

# Curl command
curl -X POST "$URL" \
     -H "Authorization: Bearer secret-random-token" \
     -H "Content-Type: application/json" \
     -d '{
         "event_type": "test_event",
         "event_author": "JohnDoe",
         "alias": "alias123",
         "artifact_version": "v1.0",
         "artifact_version_string": "1.0.0",
         "artifact_collection_name": "collection1",
         "project_name": "projectX",
         "entity_name": "entityA"
         }'
