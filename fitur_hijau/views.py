from django.shortcuts import render
from utils.query import *
import uuid
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse


# Create your views here.

def tambah_playlist(request):
    if request.method == "POST":
        try:
            result = []
            conn = initialize_connection()
            cur = conn.cursor()

            judul_playlist = request.POST.get('title', '')  
            deskripsi_playlist = request.POST.get('description', '')
            email = request.session.get('email', '')
            id_playlist = str(uuid.uuid4())
            id_user_playlist = str(uuid.uuid4())
            timestamp_now = datetime.now().strftime('%Y-%m-%d')

            add_playlist = """INSERT INTO MARMUT.PLAYLIST (id) VALUES(%s)"""
            
            cur.execute(add_playlist, (id_playlist,))

            add_user_playlist = """INSERT INTO MARMUT.USER_PLAYLIST 
                                (email_pembuat, id_user_playlist, judul, deskripsi, 
                                jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(add_user_playlist, (email, id_user_playlist, judul_playlist, deskripsi_playlist, 0, timestamp_now, id_playlist, 0))
            connection.commit()

            return HttpResponseRedirect(reverse('fitur-hijau:create_playlist.html'))

        except Exception as e:
            connection.rollback()
            
            messages.error(request, f"Failed to add playlist: {str(e)}")

            return HttpResponseRedirect(reverse('fitur_hijau:detail_playlist'))

    return render(request, "create_playlist.html")

def show_playlists(request):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    email = request.session.get('email', '')
    
    query = """SELECT judul, jumlah_lagu, total_durasi,
            id_user_playlist, id_playlist 
            FROM MARMUT.user_playlist as U
            WHERE U.email_pembuat=%s"""
    cur.execute(query, (email,))
    rows = cur.fetchall()
    
    context = {
        'rows' : rows
    }

    return render(request, "user_playlist.html", context)

def detail_playlist(request, id_playlist):
    # try:
    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    query_songs = """SELECT DISTINCT K.judul, Ak.nama, K.durasi, PS.id_song
            FROM MARMUT.PLAYLIST_SONG AS PS
            JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
            JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
            JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
            JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
            WHERE PS.id_playlist = %s"""
    
    cur.execute(query_songs, (id_playlist,))
    songses = cur.fetchall()

    query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM MARMUT.PLAYLIST_SONG AS PS
                        JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                        JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                        JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
    cur.execute(query_jumlah_songs, (id_playlist,))
    amount_songs = cur.fetchone()

    query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                        FROM (
                            SELECT DISTINCT K.judul, Ak.nama, K.durasi
                            FROM MARMUT.PLAYLIST_SONG AS PS
                            JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                            JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                            JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                            JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                            WHERE PS.id_playlist = %s
                        ) AS subquery;
                        """
    cur.execute(query_total_durasi, (id_playlist,))
    total_duration = cur.fetchone()

    jam = total_duration[0] // 60
    menit = total_duration[0] % 60

    query_details = """SELECT U.judul, U.jumlah_lagu, U.total_durasi, 
            U.tanggal_dibuat, U.deskripsi, U.id_playlist, A.nama,
            P.id_song
            FROM MARMUT.user_playlist AS U, MARMUT.akun AS A, 
            MARMUT.playlist_song AS P
            WHERE U.email_pembuat = A.email AND U.id_playlist=%s"""
    
    cur.execute(query_details, (id_playlist,))
    details = cur.fetchone()

    context = {
        'details': details,
        'songs': songses,
        'amount_songs':amount_songs,
        'total_duration':(jam,menit),
    }

    return render(request, "fitur-hijau/detail_playlist.html", context)

def ubah_playlist(request,id_playlist):

    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    ambil_id="""SELECT id_playlist
        FROM MARMUT.user_playlist
        WHERE id_playlist=%s"""
    cur.execute(ambil_id,(id_playlist,))
    id=cur.fetchone

    context={
        "id":id,
    }

    if request.method == "POST":

        judul_playlist = request.POST.get('title', '')  
        deskripsi_playlist = request.POST.get('description', '')


        edit_playlist = """UPDATE MARMUT.user_playlist
                        SET judul = %s, deskripsi = %s
                        WHERE id_playlist = %s"""
        cur.execute(edit_playlist, (judul_playlist,deskripsi_playlist,id_playlist))
        connection.commit()


        return HttpResponseRedirect(reverse('fitur-hijau:user_playlists'))

    return render(request, "ubah_playlist.html",context)

def delete_playlist(request,id_playlist):

    if request.method == "POST":

        result = []
        conn = initialize_connection()
        cur = conn.cursor()

        delete_songs = "DELETE FROM MARMUT.playlist_song WHERE id_playlist=%s"
        cur.execute(delete_songs, (id_playlist,))

        delete_query = "DELETE FROM MARMUT.user_playlist WHERE id_playlist=%s"
        cur.execute(delete_query, (id_playlist,))

        delete_playlist_utama = "DELETE FROM MARMUT.playlist WHERE id=%s"
        cur.execute(delete_playlist_utama, (id_playlist,))

        connection.commit()
        return HttpResponseRedirect(reverse('kelola_playlist:show_playlists'))

    return render(request, "user_playlist.html")

def tambah_lagu(request, id_playlist):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    available_songs_query = """SELECT K.judul, U.nama, S.id_konten
                            FROM MARMUT.konten AS K, MARMUT.song AS S, 
                            MARMUT.akun AS U, MARMUT.artist AS A
                            WHERE K.id = S.id_konten AND S.id_artist = A.id AND 
                            A.email_akun = U.email"""
    cur.execute(available_songs_query)
    rows = cur.fetchall()

    ambil_id_query = """SELECT id_playlist
                        FROM MARMUT.user_playlist
                        WHERE id_playlist=%s"""
    
    cur.execute(ambil_id_query, (id_playlist,))
    id = cur.fetchone()

    context = {
        'rows': rows,
        'id': id,
        'error_message': None
    }

    if request.method == "POST":
        id_lagu = request.POST.get('id_lagu', '')

        # Cek apakah lagu sudah ada di playlist
        check_song_query = """SELECT 1 FROM MARMUT.playlist_song
                            WHERE id_playlist = %s AND id_song = %s"""
        cur.execute(check_song_query, (id_playlist, id_lagu))
        song_exists = cur.fetchone()

        if song_exists:
            # Lagu sudah ada di playlist, tampilkan pesan error
            context['error_message'] = "Lagu sudah ada di dalam playlist."
            return render(request, "tambah_lagu.html", context)
        else:
            # Lagu belum ada di playlist, tambahkan lagu
            add_song_query = """INSERT INTO MARMUT.playlist_song
                                (id_playlist, id_song)
                                VALUES (%s, %s)"""
            cur.execute(add_song_query, (id_playlist, id_lagu))
            connection.commit()

            query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM MARMUT.PLAYLIST_SONG AS PS
                        JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                        JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                        JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
            cur.execute(query_jumlah_songs, (id_playlist,))
            amount_songs = cur.fetchone()

            edit_jumlah_songs = """UPDATE MARMUT.user_playlist
                                SET jumlah_lagu = %s
                                WHERE id_playlist = %s"""
            cur.execute(edit_jumlah_songs,(amount_songs[0],id_playlist,))
            connection.commit()

            query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                        FROM (
                            SELECT DISTINCT K.judul, Ak.nama, K.durasi
                            FROM MARMUT.PLAYLIST_SONG AS PS
                            JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                            JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                            JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                            JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                            WHERE PS.id_playlist = %s
                        ) AS subquery;
                        """
            cur.execute(query_total_durasi, (id_playlist,))
            total_duration = cur.fetchone()

            edit_durasi_songs = """UPDATE MARMUT.user_playlist
                                SET total_durasi = %s
                                WHERE id_playlist = %s"""
            cur.execute(edit_durasi_songs,(total_duration[0],id_playlist,))
            connection.commit()

            return HttpResponseRedirect(reverse('fitur-hijau:detail_playlist', args=(id_playlist,)))

    return render(request, "tambah_lagu_ke_playlist.html", context)

def delete_song(request, id_playlist, id_song):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    if request.method == "POST":

        delete_query = "DELETE FROM MARMUT.playlist_song WHERE id_song=%s AND id_playlist=%s"
        cur.execute(delete_query, (id_song,id_playlist,))

        connection.commit()

        query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM MARMUT.PLAYLIST_SONG AS PS
                        JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                        JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                        JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
        cur.execute(query_jumlah_songs, (id_playlist,))
        amount_songs = cur.fetchone()

        edit_jumlah_songs = """UPDATE MARMUT.user_playlist
                            SET jumlah_lagu = %s
                            WHERE id_playlist = %s"""
        cur.execute(edit_jumlah_songs,(amount_songs[0],id_playlist,))
        connection.commit()

        query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM MARMUT.PLAYLIST_SONG AS PS
                        JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                        JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                        JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
        cur.execute(query_total_durasi, (id_playlist,))
        total_duration = cur.fetchone()

        edit_durasi_songs = """UPDATE MARMUT.user_playlist
                            SET total_durasi = %s
                            WHERE id_playlist = %s"""
        cur.execute(edit_durasi_songs,(total_duration[0],id_playlist,))
        connection.commit()
        return HttpResponseRedirect(reverse('fitur-hijau:detail_playlist.html', args=(id_playlist,)))

    return render(request, "detail_playlist.html")

def detail_song(request,id_song):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()
    
    query_judul_song = """SELECT K.judul, K.tanggal_rilis, K.tahun, K.durasi, S.total_play,
                        S.total_download
                        FROM MARMUT.konten AS K, MARMUT.song AS S
                        WHERE S.id_konten = K.id AND K.id=%s"""
    cur.execute(query_judul_song, (id_song,))
    detail=cur.fetchone()

    query_artist = """SELECT Ak.nama
                    FROM MARMUT.artist AS Ar, MARMUT.akun AS Ak, MARMUT.song AS S
                    WHERE S.id_artist=Ar.id AND Ar.email_akun=Ak.email AND S.id_konten=%s"""
    cur.execute(query_artist, (id_song,))
    artist=cur.fetchone()

    query_songwriter="""SELECT DISTINCT Ak.nama
                    FROM MARMUT.songwriter AS S, MARMUT.songwriter_write_song AS SWS,
                    MARMUT.konten AS K, MARMUT.akun AS Ak
                    WHERE SWS.id_song=%s AND SWS.id_songwriter=S.id AND S.email_akun=Ak.email"""
    cur.execute(query_songwriter,(id_song,))
    songwriter=cur.fetchall()

    query_album="""SELECT A.judul
                FROM MARMUT.album AS A, MARMUT.song AS S
                WHERE S.id_konten=%s AND S.id_album=A.id"""
    cur.execute(query_album,(id_song,))
    album=cur.fetchone()

    query_genre="""SELECT G.genre
                FROM MARMUT.genre AS G, MARMUT.konten AS K
                WHERE G.id_konten=%s AND G.id_konten=K.id"""
    cur.execute(query_genre,(id_song,))
    genre=cur.fetchall()

    get_id="""SELECT K.id
            FROM MARMUT.konten AS K, MARMUT.SONG AS S
            WHERE S.id_konten=%s AND S.id_konten=K.id"""
    cur.execute(get_id,(id_song,))
    id_get=cur.fetchone()

    context = {
        'detail_a':detail,
        'detail_b':artist,
        'detail_c':songwriter,
        'detail_d':album,
        'detail_e':genre,
        'get_id':id_get
    }

    return render(request, "detail_song.html", context)

def add_song_to_playlist(request,id_song):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    query_judul_song = """SELECT K.judul
                        FROM MARMUT.konten AS K, MARMUT.song AS S
                        WHERE S.id_konten = K.id AND K.id=%s"""
    cur.execute(query_judul_song,(id_song,))
    deksripsi=cur.fetchone()

    query_penyanyi = """SELECT Ak.nama
                    FROM MARMUT.artist AS Ar, MARMUT.akun AS Ak, MARMUT.song AS S
                    WHERE S.id_artist=Ar.id AND Ar.email_akun=Ak.email AND S.id_konten=%s"""
    cur.execute(query_penyanyi, (id_song,))
    artist=cur.fetchone()

    email = request.session.get('email', '')

    query_pilihan = """SELECT U.judul, U.id_playlist
                    FROM MARMUT.user_playlist AS U
                    WHERE U.email_pembuat=%s"""
    cur.execute(query_pilihan, (email,))
    detail=cur.fetchall()

    get_id="""SELECT K.id
            FROM MARMUT.konten AS K, MARMUT.SONG AS S
            WHERE S.id_konten=%s AND S.id_konten=K.id"""
    cur.execute(get_id,(id_song,))
    id_get=cur.fetchone()

    context={
        'judul':deksripsi,
        'artist':artist,
        'playlists':detail,
        'id':id_get,
    }

    if request.method == "POST":

        id_playlist = request.POST.get('id_playlist', '')

        check_song_query = """SELECT 1 FROM MARMUT.playlist_song
                            WHERE id_playlist = %s AND id_song = %s"""
        cur.execute(check_song_query, (id_playlist, id_song))
        song_exists = cur.fetchone()

        if song_exists:
            # Lagu sudah ada di playlist, tampilkan pesan error
            context['error_message'] = "Lagu dengan ada di dalam playlist."
            return render(request, "tambah_lagu_ke_playlist.html", context)
        else:
            add_to_playlist = """INSERT INTO MARMUT.playlist_song
                                    (id_playlist, id_song) 
                                    VALUES (%s, %s)"""
            cur.execute(add_to_playlist, (id_playlist, id_song,))
            connection.commit()

            query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM MARMUT.PLAYLIST_SONG AS PS
                        JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                        JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                        JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
            cur.execute(query_jumlah_songs, (id_playlist,))
            amount_songs = cur.fetchone()

            edit_jumlah_songs = """UPDATE MARMUT.user_playlist
                                SET jumlah_lagu = %s
                                WHERE id_playlist = %s"""
            cur.execute(edit_jumlah_songs,(amount_songs[0],id_playlist,))
            connection.commit()

            query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                        FROM (
                            SELECT DISTINCT K.judul, Ak.nama, K.durasi
                            FROM MARMUT.PLAYLIST_SONG AS PS
                            JOIN MARMUT.SONG AS S ON PS.id_song = S.id_konten
                            JOIN MARMUT.KONTEN AS K ON S.id_konten = K.id
                            JOIN MARMUT.ARTIST AS Ar ON S.id_artist = Ar.id
                            JOIN MARMUT.akun AS Ak ON Ar.email_akun = Ak.email
                            WHERE PS.id_playlist = %s
                        ) AS subquery;
                        """
            cur.execute(query_total_durasi, (id_playlist,))
            total_duration = cur.fetchone()

            edit_durasi_songs = """UPDATE MARMUT.user_playlist
                                SET total_durasi = %s
                                WHERE id_playlist = %s"""
            cur.execute(edit_durasi_songs,(total_duration[0],id_playlist,))
            connection.commit()
            return HttpResponseRedirect(reverse('fitur-hijau:detail_song', args=(id_song,)))

    return render(request, "add_song_to_user_playlist.html",context)

def play_song(request,id_song):
    if request.method == "POST":
        
        timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return HttpResponseRedirect(reverse('fitur-hijau:create_playlist.html'))

    return render(request, "playlist_detail.html")

def show_no_playlist(request):
    return render(request, "no_playlist.html", {})

def show_user_playlist(request):
    return render(request, "user_playlist.html", {})

def show_create_playlist(request):
    return render(request, "create_playlist.html", {})

def show_detail_playlist(request):
    return render(request, "detail_playlist.html", {})

def show_tambah_lagu(request):
    return render(request, "tambah_lagu.html", {})

def show_detail_song(request):
    return render(request, "detail_song.html", {})

def show_play_song(request):
    return render(request, "play_song.html", {})

def show_tambah_lagu_ke_playlist(request):
    return render(request, "tambah_lagu_ke_playlist.html", {})

def show_tambah_lagu_ke_playlist_success(request):
    return render(request, "tambah_lagu_ke_playlist_success.html", {})

def show_tambah_download_success(request):
    return render(request, "tambah_download_success.html", {})

def show_detail_playlist_shuffle(request):
    return render(request, "detail_playlist_shuffle.html", {})