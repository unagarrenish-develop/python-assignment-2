"""Q4: Safe SQL join query builder. Accepts JSON on stdin; prints SQL and parameters.
No query is executed. Use a database connector to execute the returned SQL safely.
"""
import json
import sys

TABLE_COLUMNS = {
    "student": {"id": "s.student_id", "name": "s.name", "spi": "s.spi"},
    "course": {"id": "c.course_id", "name": "c.name"},
    "registration": {"student_id": "r.student_id", "course_id": "r.course_id"}
}
ALIASES = {"student": "s", "course": "c", "registration": "r"}
OPS = {"=", "!=", ">", ">=", "<", "<=", "LIKE"}

def validate_field(field):
    if not isinstance(field, str) or "." not in field:
        raise ValueError(f"Invalid field: {field}")
    table, column = field.split(".", 1)
    if table not in TABLE_COLUMNS or column not in TABLE_COLUMNS[table]:
        raise ValueError(f"Field is not whitelisted: {field}")
    return TABLE_COLUMNS[table][column]

def build_query(spec):
    columns = spec.get("columns", [])
    if not columns: raise ValueError("At least one projection column is required")
    projection = ", ".join(validate_field(c) for c in columns)
    sql = ("SELECT " + projection +
           " FROM Student s JOIN CourseRegistration r ON s.student_id=r.student_id "
           "JOIN Course c ON c.course_id=r.course_id")
    params, clauses = [], []
    for item in spec.get("where", []):
        field, operator, value = item.get("column"), item.get("op"), item.get("value")
        if operator not in OPS: raise ValueError("Unsupported filter operator")
        clauses.append(validate_field(field) + " " + operator + " %s")
        params.append(value)
    if clauses: sql += " WHERE " + " AND ".join(clauses)
    order = spec.get("order_by")
    if order:
        field = validate_field(order.get("column"))
        direction = order.get("direction", "ASC").upper()
        if direction not in ("ASC", "DESC"): raise ValueError("Sort direction must be ASC or DESC")
        sql += f" ORDER BY {field} {direction}"
    limit = int(spec.get("limit", 100))
    if not 1 <= limit <= 1000: raise ValueError("LIMIT must be between 1 and 1000")
    sql += " LIMIT %s"
    params.append(limit)
    return sql, params

def main():
    try:
        spec = json.load(sys.stdin)
        sql, params = build_query(spec)
        print("SQL_OK")
        print(sql)
        print("PARAMS", json.dumps(params, ensure_ascii=False))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f"SQL_INVALID: {exc}")

if __name__ == "__main__":
    main()
