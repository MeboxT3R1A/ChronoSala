from werkzeug.security import generate_password_hash

senha = 'prof123'
hash = generate_password_hash(senha)

print(f"Hash da senha: {hash}")
