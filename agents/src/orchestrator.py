import asyncio
import logging
import os
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


async def main():
    cfg = load_config()

    from agents.quality_agent import QualityAgent
    from agents.maintenance_agent import MaintenanceAgent
    from agents.production_agent import ProductionAgent

    machine_ids = ["cnc_001", "conv_001", "robot_001"]

    quality = QualityAgent(
        machine_ids=machine_ids,
        model=cfg["agents"]["quality"]["model"],
    )
    maintenance = MaintenanceAgent(
        machine_ids=machine_ids,
        model=cfg["agents"]["maintenance"]["model"],
    )
    production = ProductionAgent(
        model=cfg["agents"]["production"]["model"],
    )

    logger.info("Starting A2A agent orchestrator")
    await asyncio.gather(
        quality.run_loop(cfg["agents"]["quality"]["poll_interval_seconds"]),
        maintenance.run_loop(cfg["agents"]["maintenance"]["poll_interval_seconds"]),
        production.run_loop(cfg["agents"]["production"]["poll_interval_seconds"]),
    )


if __name__ == "__main__":
    asyncio.run(main())
