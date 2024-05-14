from flask import Flask, render_template, request, redirect, url_for
import client

app = Flask(__name__)

@app.route('/')
def index():
    data_siswa = client.dapatkan_semua_siswa()
    return render_template('index.html', data_siswa=data_siswa)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_siswa():
    if request.method == 'POST':
        nama = request.form['nama']
        nilai = float(request.form['nilai'])
        client.tambah_siswa(nama, nilai)
        return redirect(url_for('index'))
    return render_template('tambah.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_siswa(id):
    siswa = client.dapatkan_siswa_by_id(id)
    if siswa.id == 0:
        return render_template('404.html'), 404
    if request.method == 'POST':
        nama = request.form['nama']
        nilai = float(request.form['nilai'])
        client.perbarui_siswa(id, nama, nilai)
        return redirect(url_for('index'))
    return render_template('edit.html', siswa=siswa)

@app.route('/hapus/<int:id>', methods=['POST'])
def hapus_siswa(id):
    client.hapus_siswa(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
