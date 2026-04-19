import os
import xmlrpc.client


class OdooConnector:
    def __init__(self):
        self.url = os.getenv("ODOO_URL", "http://localhost:8069")
        self.db = os.getenv("ODOO_DB", "integrated_factory_mes")
        self.username = os.getenv("ODOO_USER", "admin")
        self.password = os.getenv("ODOO_PASSWORD", "admin")
        self._uid: int | None = None

    def _authenticate(self) -> int:
        if self._uid is None:
            common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
            self._uid = common.authenticate(self.db, self.username, self.password, {})
        return self._uid

    def _models(self):
        return xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")

    def upsert_machine_status(self, machine_id: str, is_running: bool, error_code: int, telemetry_json: str):
        uid = self._authenticate()
        models = self._models()
        model = "integrated_factory.machine_status"

        existing = models.execute_kw(
            self.db, uid, self.password, model, "search",
            [[["machine_id", "=", machine_id]]]
        )

        vals = {
            "machine_id": machine_id,
            "is_running": is_running,
            "error_code": error_code,
            "telemetry_json": telemetry_json,
        }

        if existing:
            models.execute_kw(self.db, uid, self.password, model, "write", [existing, vals])
        else:
            models.execute_kw(self.db, uid, self.password, model, "create", [vals])
