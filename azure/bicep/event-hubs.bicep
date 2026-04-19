param namespaceName string
param location string
param skuName string = 'Standard'

resource eventHubNamespace 'Microsoft.EventHub/namespaces@2023-01-01-preview' = {
  name: namespaceName
  location: location
  sku: {
    name: skuName
    tier: skuName
    capacity: 1
  }
}

resource machineMetricsHub 'Microsoft.EventHub/namespaces/eventhubs@2023-01-01-preview' = {
  parent: eventHubNamespace
  name: 'machine-metrics'
  properties: {
    partitionCount: 8
    messageRetentionInDays: 1
  }
}

resource alertsHub 'Microsoft.EventHub/namespaces/eventhubs@2023-01-01-preview' = {
  parent: eventHubNamespace
  name: 'factory-alerts'
  properties: {
    partitionCount: 2
    messageRetentionInDays: 7
  }
}

output namespaceName string = eventHubNamespace.name
