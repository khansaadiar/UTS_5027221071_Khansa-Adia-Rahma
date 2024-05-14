import grpc
from concurrent import futures
import time
import psycopg2
import siswa_pb2
import siswa_pb2_grpc

DATABASE = "nama_database"
USER = "nama_pengguna"
PASSWORD = "kata_sandi"
HOST = "localhost"
PORT = "5432"

class SiswaService(siswa_pb2_grpc.SiswaServiceServicer):
    def __init__(self):
        self.conn = psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        self.cur = self.conn.cursor()

    def TambahSiswa(self, request, context):
        query = "INSERT INTO siswa (nama, nilai) VALUES (%s, %s) RETURNING id;"
        self.cur.execute(query, (request.nama, request.nilai))
        siswa_id = self.cur.fetchone()[0]
        self.conn.commit()
        return siswa_pb2.Siswa(id=siswa_id, nama=request.nama, nilai=request.nilai)

    def DapatkanSiswaById(self, request, context):
        query = "SELECT nama, nilai FROM siswa WHERE id = %s;"
        self.cur.execute(query, (request.id,))
        result = self.cur.fetchone()
        if result:
            nama, nilai = result
            return siswa_pb2.Siswa(id=request.id, nama=nama, nilai=nilai)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Siswa tidak ditemukan.")
            return siswa_pb2.Siswa()

    def PerbaruiSiswa(self, request, context):
        query = "UPDATE siswa SET nama = %s, nilai = %s WHERE id = %s;"
        self.cur.execute(query, (request.nama, request.nilai, request.id))
        self.conn.commit()
        return request

    def HapusSiswa(self, request, context):
        query = "DELETE FROM siswa WHERE id = %s RETURNING nama, nilai;"
        self.cur.execute(query, (request,))
        result = self.cur.fetchone()
        if result:
            nama, nilai = result
            return siswa_pb2.Siswa(id=request, nama=nama, nilai=nilai)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Siswa tidak ditemukan.")
            return siswa_pb2.Siswa()

    def SemuaSiswa(self, request, context):
        query = "SELECT id, nama, nilai FROM siswa;"
        self.cur.execute(query)
        for row in self.cur.fetchall():
            yield siswa_pb2.Siswa(id=row[0], nama=row[1], nilai=row[2])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    siswa_pb2_grpc.add_SiswaServiceServicer_to_server(SiswaService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
