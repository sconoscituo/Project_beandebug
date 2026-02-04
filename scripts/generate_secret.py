import secrets
import string

def generate_secret_key(length=50):
    """안전한 시크릿 키 생성"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("Generated SECRET_KEY:")
    print(generate_secret_key())