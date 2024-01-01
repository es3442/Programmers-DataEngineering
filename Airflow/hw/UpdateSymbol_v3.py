def get_historical_prices(symbol):
    ticket = yf.Ticker(symbol)
    data = ticket.history()
    records = []
    for index, row in data.iterrows():
        date = index.strftime('%Y-%m-%d %H:%M:%S')
        records.append([date, row["Open"], row["High"],
                       row["Low"], row["Close"], row["Volume"]])
    return records


@task
def load(schema, table, records):
    logging.info("load started")
    cur = get_Redshift_connection()
    # 원본 테이블이 없으면 생성 - 테이블이 처음 한번 만들어질 때 필요한 코드
    create_table_sql = f"""CREATE TABLE IF NOT EXISTS {schema}.{table} (
    date date,
    "open" float,
    high float,
    low float,
    close float,
    volume bigint,
    created_date timestamp DEFAULT GETDATE()
    );"""
    cur.execute(create_table_sql)
    logging.info(create_table_sql)

    try:
        cur.execute("BEGIN;")
        # 임시 테이블로 원본 테이블을 복사
        cur.execute(f"CREATE TEMP TABLE t AS SELECT * FROM {schema}.{table};")
        logging.info("create temp table")
        # 새 레코드 추가
        for r in records:
            sql = f"INSERT INTO t VALUES ('{r[0]}', {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]});"
            print(sql)
            cur.execute(sql)

        # 임시 테이블 내용을 원본 테이블로 복사
        cur.execute(f"DELETE FROM {schema}.{table};")
        cur.execute(f"""INSERT INTO {schema}.{table}
                    SELECT date, "open", high, low, close, volume FROM (
                    SELECT *, ROW_NUMBER() OVER (PARTITION BY date ORDER BY created_date DESC) seq
                    FROM t
                    )
                    WHERE seq = 1;""")
        cur.execute("COMMIT;")   # cur.execute("END;")
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise
    logging.info("load done")


with DAG(
    dag_id='UpdateSymbol_v3',
    start_date=datetime(2023, 5, 30),
    catchup=False,
    tags=['API'],
    schedule='0 10 * * *'
) as dag:

    results = get_historical_prices("AAPL")
    load("es3442", "stock_info_v3", results)
