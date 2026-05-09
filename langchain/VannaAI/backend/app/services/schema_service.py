from __future__ import annotations

from app.models import SchemaColumn
from app.services.query_service import QueryService


TABLE_DESCRIPTIONS = {
    "customers": "客户表，包含城市、会员等级和注册日期。",
    "products": "商品表，包含品类、成本价和标价。",
    "orders": "订单主表，包含客户、订单编号、订单状态和下单时间。",
    "order_items": "订单明细表，包含商品、数量、成交单价和优惠金额。",
    "payments": "支付表，包含支付方式、支付状态、实付金额和支付时间。",
    "refunds": "退款表，包含退款原因、退款金额和退款时间。",
}


METRIC_HINTS = """
常用指标:
- GMV = SUM(order_items.quantity * order_items.unit_price - order_items.discount_amount)
- 利润 = SUM(order_items.quantity * (order_items.unit_price - products.cost_price) - order_items.discount_amount)
- 客单价 = GMV / 订单数
- 退款率 = 退款订单数 / 支付成功订单数
- 只统计有效交易时，优先使用 orders.order_status IN ('paid', 'shipped', 'completed')
""".strip()


class SchemaService:
    def __init__(self, query_service: QueryService, business_tables: list[str]) -> None:
        self.query_service = query_service
        self.business_tables = business_tables

    def list_columns(self) -> list[SchemaColumn]:
        rows = self.query_service.fetch_all(
            """
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = ANY(%s)
            ORDER BY table_name, ordinal_position
            """,
            (self.business_tables,),
        )
        return [
            SchemaColumn(
                table_name=row["table_name"],
                column_name=row["column_name"],
                data_type=row["data_type"],
                is_nullable=row["is_nullable"] == "YES",
            )
            for row in rows
        ]

    def list_foreign_keys(self) -> list[dict[str, str]]:
        return self.query_service.fetch_all(
            """
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_name = ANY(%s)
            ORDER BY tc.table_name, kcu.column_name
            """,
            (self.business_tables,),
        )

    def build_prompt_context(self) -> str:
        columns = self.list_columns()
        foreign_keys = self.list_foreign_keys()
        lines: list[str] = ["业务数据库表结构:"]

        for table in self.business_tables:
            lines.append(f"\n表 {table}: {TABLE_DESCRIPTIONS.get(table, '')}")
            for column in [col for col in columns if col.table_name == table]:
                nullable = "nullable" if column.is_nullable else "not null"
                lines.append(f"- {column.column_name}: {column.data_type}, {nullable}")

        if foreign_keys:
            lines.append("\n外键关系:")
            for fk in foreign_keys:
                lines.append(
                    "- "
                    f"{fk['table_name']}.{fk['column_name']} -> "
                    f"{fk['foreign_table_name']}.{fk['foreign_column_name']}"
                )

        lines.append("\n" + METRIC_HINTS)
        return "\n".join(lines)
