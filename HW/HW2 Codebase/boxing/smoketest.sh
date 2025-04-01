#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

###############################################
#
# Boxer Management
#
###############################################

create_boxer() {
  name=$1
  weight=$2
  height=$3
  reach=$4
  age=$5

  echo "Creating boxer ($name, $weight lbs)..."
  curl -s -X POST "$BASE_URL/create-boxer" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\", \"weight\":$weight, \"height\":$height, \"reach\":$reach, \"age\":$age}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Boxer added successfully."
  else
    echo "Failed to add boxer."
    exit 1
  fi
}

get_boxer_by_id() {
  boxer_id=$1

  echo "Getting boxer by ID ($boxer_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-boxer-by-id/$boxer_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer retrieved successfully by ID ($boxer_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Boxer JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get boxer by ID ($boxer_id)."
    exit 1
  fi
}

delete_boxer() {
  boxer_id=$1

  echo "Deleting boxer by ID ($boxer_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-boxer/$boxer_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer deleted successfully by ID ($boxer_id)."
  else
    echo "Failed to delete boxer by ID ($boxer_id)."
    exit 1
  fi
}

###############################################
#
# Ring Management
#
###############################################

enter_ring() {
  boxer_id=$1

  echo "Boxer $boxer_id entering the ring..."
  response=$(curl -s -X POST "$BASE_URL/enter-ring/$boxer_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer entered the ring successfully."
  else
    echo "Failed to enter the ring."
    exit 1
  fi
}

start_fight() {
  echo "Starting a fight..."
  response=$(curl -s -X POST "$BASE_URL/fight")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Fight completed successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Fight result:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to complete the fight."
    exit 1
  fi
}

# Run the tests
check_health
check_db

# Create boxers
create_boxer "Bob" 220 71 71.0 25
create_boxer "Dave" 210 75 78.0 30

# Get boxer by ID
get_boxer_by_id 1

# Test a fight
enter_ring 1
enter_ring 2
start_fight

# Test deleting a boxer
delete_boxer 1

echo "All tests passed successfully!"