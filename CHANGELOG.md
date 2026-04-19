# Changelog

All notable changes to IntegratedFactory are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

<!-- PRs targeting this release are listed below automatically -->

---

## [0.1.0] — 2026-04-19

### Added
- [#25](https://github.com/BiplabGH/IntegratedFactory/pull/25) fix: skip Oryx build for static site (@BiplabGH)
- [#15](https://github.com/BiplabGH/IntegratedFactory/pull/15) Bs if feat/changelog and versions (@BiplabGH)
- Animated "coming soon" landing page (`index.html`) with particle network, HUD status indicators, and progress bar
- OPC-UA simulator for CNC, conveyor, and robot arm machines
- MQTT broker configuration (EMQX + Solace) with OPC-UA bridge
- Kafka streams processor and aggregator
- InfluxDB and TimescaleDB historian writers
- MCP server (TypeScript) exposing machines, historian, and MES tools
- A2A agent framework — production, maintenance, and quality agents
- Odoo MES connector and custom `integrated_factory` addon
- Azure Bicep IaC for IoT Hub and Event Hubs
- Kubernetes Helm chart with staging and prod value sets
- Azure Static Web Apps CI/CD workflow (staging + master deploy)
- Full project documentation (architecture, data-flow, API reference, getting started)

[Unreleased]: https://github.com/BiplabGH/IntegratedFactory/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/BiplabGH/IntegratedFactory/releases/tag/v0.1.0
