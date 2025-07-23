import pymysql

print("Tentando conectar...")

try:
    conexao = pymysql.connect(
        host="localhost",
        user="root",
        password="@!r3t3l2pXEM",
        database="myteste",
        port=3306
    )
    print("✅ Conexão bem-sucedida com PyMySQL.")
    with conexao.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        versao = cursor.fetchone()
        print(f"MySQL version: {versao[0]}")
    conexao.close()

except Exception as e:
    print(f"Erro na conexão: {e}")
