from werkzeug.security import generate_password_hash

senha = 'coord132'
hash = generate_password_hash(senha)

print(f"Hash da senha: {hash}")
