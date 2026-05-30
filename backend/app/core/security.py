from passlib.context import CryptContext

# 配置 bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# 加密密码
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 验证密码
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )