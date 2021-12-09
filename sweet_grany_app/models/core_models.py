from sqlalchemy import create_engine, text

engine = create_engine("postgresql://localhost:5432/sweet_granny_test",
                       echo=True, future=True)

with engine.connect() as conn:
    res = conn.execute(text('SELECT * FROM tags'))

print(res.all())
