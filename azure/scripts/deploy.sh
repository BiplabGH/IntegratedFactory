#!/bin/bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-intfactory-rg}"
LOCATION="${LOCATION:-eastus}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

echo "Deploying IntegratedFactory Azure infrastructure..."
echo "  Resource Group : $RESOURCE_GROUP"
echo "  Location       : $LOCATION"
echo "  Environment    : $ENVIRONMENT"

az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file "$(dirname "$0")/../bicep/main.bicep" \
  --parameters environment="$ENVIRONMENT" \
  --output table

echo "Deployment complete."
