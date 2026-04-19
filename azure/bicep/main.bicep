targetScope = 'resourceGroup'

param location string = resourceGroup().location
param prefix string = 'intfactory'
param environment string = 'dev'

module iotHub 'iot-hub.bicep' = {
  name: 'iot-hub-deploy'
  params: {
    location: location
    name: '${prefix}-iothub-${environment}'
  }
}

module eventHubs 'event-hubs.bicep' = {
  name: 'event-hubs-deploy'
  params: {
    location: location
    namespaceName: '${prefix}-eventhubs-${environment}'
  }
}

output iotHubConnectionString string = iotHub.outputs.connectionString
output eventHubsNamespace string = eventHubs.outputs.namespaceName
