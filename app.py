import streamlit as st
from sqlalchemy import text

list_maskapai = ['', 'Amelia Airlines', 'HaykalAir', 'AirRindah', 'Ratna Airlines', 'AbghazAir']
list_kode = ['', 'AK009', 'FH027', 'AM088', 'RM097', 'AB100']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://AmeliaKurnia:AyZa67mtESxw@ep-morning-glade-50476120.us-east-2.aws.neon.tech/fp3")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS AIRPORT (id serial, nama_maskapai varchar, nama_pilot varchar, kode_penerbangan char(25), \
                                                       kelas text, bandara_asal varchar, bandara_tujuan text, tanggal date);')
    session.execute(query)

st.header("FlyTrack Group Four'S Data Management System")
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM airport ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

    st.markdown("## Kelompok 4:")
    st.markdown("1. Amelia Kurnia Fitri (2043221009)")
    st.markdown("2. Fhikri Haykal Oktarianto (2043221027)")
    st.markdown("3. Arindah Maharani Saputri (2043221088)")
    st.markdown("4. Ratna Maulidah Wulandari (2043221097)")
    st.markdown("5. Abghaza Bayu Kusuma W. P. (2043221100)")

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO airport (nama_maskapai, nama_pilot, kode_penerbangan, kelas, bandara_asal, bandara_tujuan, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM airport ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_maskapai_lama = result["nama_maskapai"]
        nama_pilot_lama = result["nama_pilot"]
        kode_penerbangan_lama = result["kode_penerbangan"]
        kelas_lama = result["kelas"]
        bandara_asal_lama = result["bandara_asal"]
        bandara_tujuan_lama = result["bandara_tujuan"]
        waktu_lama = result["waktu"]
        tanggal_lama = result["tanggal"]

        with st.expander(f'a.n. {nama_pilot_lama}'):
            with st.form(f'data-{id}'):
                nama_maskapai_baru = st.selectbox("nama_maskapai", list_maskapai, list_maskapai.index(nama_maskapai_lama))
                nama_pilot_baru = st.text_input("nama_pilot", nama_pilot_lama)
                kode_penerbangan_baru = st.selectbox("kode_penerbangan", list_kode, list_kode.index(kode_penerbangan_lama))
                default_kelas = eval(kelas_lama) if eval(kelas_lama) and isinstance(eval(kelas_lama), list) else []
                kelas_baru = st.multiselect("kelas", ['economy', 'comfort', 'business', 'amatiran'], default=list(set(default_kelas) & set(['economy', 'comfort', 'business', 'amatiran'])))
                bandara_asal_baru = st.text_input("bandara_asal", bandara_asal_lama)
                bandara_tujuan_baru = st.text_input("bandara_tujuan", bandara_tujuan_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE airport \
                                          SET nama_maskapai=:1, nama_pilot=:2, kode_penerbangan=:3, kelas=:4, \
                                          bandara_asal=:5, bandara_tujuan=:6, waktu=:7, tanggal=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':nama_maskapai_baru, '2':nama_pilot_baru, '3':kode_penerbangan_baru, '4':str(kelas_baru), 
                                                    '5':bandara_asal_baru, '6':bandara_tujuan_baru, '7':waktu_baru, '8':tanggal_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM airport WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()
