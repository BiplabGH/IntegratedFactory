# Version History

IntegratedFactory uses [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Version | Date       | Status  | Notes                              |
|---------|------------|---------|------------------------------------|
| 0.1.0   | 2026-04-19 | Current | Initial platform scaffold & launch page |

---

## Version Policy

| Bump    | When to use                                                        |
|---------|--------------------------------------------------------------------|
| `PATCH` | Bug fixes, doc corrections, config tweaks — no API/schema change  |
| `MINOR` | New features, new agents/tools, new integrations — backward-compatible |
| `MAJOR` | Breaking changes to APIs, schemas, or data contracts              |

---

## How to cut a release

1. Update `[Unreleased]` section in [CHANGELOG.md](CHANGELOG.md) with the new version and date
2. Add a row to the table above
3. Create and push a git tag:
   ```sh
   git tag -a v0.2.0 -m "release: v0.2.0"
   git push origin v0.2.0
   ```
4. GitHub Actions will deploy to production on tag push

---

## Roadmap targets

| Version | Target     | Scope                                        |
|---------|------------|----------------------------------------------|
| 0.2.0   | TBD        | Live OPC-UA data ingestion via EMQX          |
| 0.3.0   | TBD        | MES work-order dashboard in Odoo             |
| 0.4.0   | TBD        | A2A agent orchestration with MCP tools live  |
| 1.0.0   | TBD        | Production-ready, full Azure deployment      |
