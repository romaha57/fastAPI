from fastapi.middleware.cors import CORSMiddleware
from main import app, origins


# middleware на защиту от CORS атак
app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', "OPTIONS"],
    alllow_headers=[
        'Content-Type',
        'Set-Cookie',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin',
        'Authorization',
    ]
)
