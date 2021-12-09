# import os
#
# from sqlalchemy import create_engine, text
#
# # engine = create_engine("postgresql://localhost:5432/sweet_granny",
# #                        echo=True, future=True)
# #
# # with engine.connect() as conn:
# #     res = conn.execute(text('SELECT * FROM tags'))
# #     conn.commit()
# #
# # print(res.all())
#
#
# class CoreDBHandler:
#
#     def __init__(self, db_path, db_name):
#         self.db_path = db_path
#         self.db_name = db_name
#
#     def execute(self, commands: list):
#         engine = self._create_engine()
#         with engine.connect() as conn:
#             for command in commands:
#                 res = conn.execute(text(command))
#             conn.commit()
#         return res
#
#     # def __enter__(self):
#     #     self.connection = self._create_engine().connect()
#     #     return self.connection
#     #
#     # def __exit__(self, exc_type, exc_val, exc_tb):
#     #     self.connection.commit()
#     #     self.connection.close()
#     #     if exc_val:
#     #         raise exc_type(exc_val)
#
#     def _create_engine(self):
#         return create_engine(self._db_route())
#
#     def _db_route(self):
#         return os.path.join(self.db_path, self.db_name)
#
#
# if __name__ == '__main__':
#     handler = CoreDBHandler(
#         'postgresql://localhost:5432', 'sweet_granny'
#     )
#     res = handler.execute(text('SELECT * FROM tags'))
#
#     print(res)
