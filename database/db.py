import grpc
from concurrent import futures
import time
import psycopg2
import siswa_pb2
import siswa_pb2_grpc

# Informasi koneksi database PostgreSQL
DATABASE = "nama_database"
USER = "root"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"

# Implementasi dari service SiswaService
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
        # Implementasi logika tambah siswa ke database
        pass

    def DapatkanSiswaById(self, request, context):
        # Implementasi logika dapatkan siswa by ID dari database
        pass

    def PerbaruiSiswa(self, request, context):
        # Implementasi logika perbarui data siswa di database
        pass

    def HapusSiswa(self, request, context):
        # Implementasi logika hapus siswa dari database
        pass

    def SemuaSiswa(self, request, context):
        # Implementasi logika dapatkan semua siswa dari database
        pass

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
