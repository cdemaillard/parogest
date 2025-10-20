import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="parogest_dev",
        user="parogest_user",
        password="parogest_dev_password"
    )
    print("✅ Connexion réussie !")
    conn.close()
except Exception as e:
    print(f"❌ Erreur : {e}")