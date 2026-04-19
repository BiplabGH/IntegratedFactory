{
    "name": "Integrated Factory MES",
    "version": "17.0.1.0.0",
    "category": "Manufacturing",
    "summary": "MES extensions for IntegratedFactory IoT platform",
    "description": """
        Connects Odoo MES with OPC-UA machine data via Kafka.
        Provides real-time machine status on work orders.
    """,
    "author": "IntegratedFactory",
    "depends": ["mrp", "maintenance"],
    "data": [
        "views/work_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
