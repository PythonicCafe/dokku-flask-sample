from db import execute_query


# Para simplificar, as migrações serão idempotentes (mesmo que executemos os SQLs abaixo em todas as releases, o estado
# final do banco será sempre o mesmo, ou seja, se as tabelas não existirem elas serão criadas e se já existirem nada
# será feito).
sqls = [
    "CREATE TABLE IF NOT EXISTS dengue (data DATE, casos INT, populacao INT)",
    "CREATE TABLE IF NOT EXISTS log_captura (datahora TIMESTAMPTZ, registros INT)",
]
for index, sql in enumerate(sqls, start=1):
    print(f"Executing SQL {index}/{len(sqls)}")
    execute_query(sql)
