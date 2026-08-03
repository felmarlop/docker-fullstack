RESERVED_SYSTEM_USERNAMES = {
    "admin",
    "administrator",
    "root",
    "system",
    "api",
    "support",
    "help",
    "staff",
    "team",
    "moderator",
    "official",
}

RESERVED_ROUTE_USERNAMES = {
    "login",
    "logout",
    "register",
    "signup",
    "profile",
    "account",
    "settings",
    "dashboard",
    "users",
    "user",
    "docs",
    "swagger",
    "redoc",
    "oauth",
    "search",
    "health",
}

RESERVED_PROJECT_USERNAMES = {
    "dockerfullstack",
    "docker-fullstack",
}

RESERVED_USERNAMES = (
    RESERVED_SYSTEM_USERNAMES | RESERVED_ROUTE_USERNAMES | RESERVED_PROJECT_USERNAMES
)

RESERVED_PREFIXES = (
    "admin",
    "root",
    "system",
)
