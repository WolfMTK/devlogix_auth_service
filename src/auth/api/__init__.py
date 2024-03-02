from .routers import tokens, users

routers = (users.router,
           tokens.router)
