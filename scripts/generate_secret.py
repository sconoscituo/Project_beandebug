import secrets

print("DB_PASSWORD:", secrets.token_urlsafe(24))
print("SECRET_KEY:", secrets.token_urlsafe(48))
