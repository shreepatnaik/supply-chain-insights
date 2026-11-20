import json
from sqlalchemy import text
from core.db import get_engine


def record_decision(thread_id, method, forecast, reason, attempts, approved):
    query = text("""
                    INSERT INTO forecast_decisions (thread_id, method, forecast, reason, attempts, approved)
                    VALUES (:thread_id, :method, :forecast, :reason, :attempts, :approved)""")

    with get_engine().begin() as conn:
        conn.execute(query, {
            "thread_id": thread_id,
            "method": method,
            "forecast": json.dumps(forecast),
            "reason": reason,
            "attempts": attempts,
            "approved": approved,
        })