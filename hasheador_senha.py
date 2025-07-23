from werkzeug.security import generate_password_hash

senha = '12345'
hash = generate_password_hash(senha)

print(f"Hash da senha: {hash}")
