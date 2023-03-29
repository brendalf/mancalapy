import os

from mancala_backend.server import create_server, define_routes, define_socket_routes

if __name__ == "__main__":
    env = os.getenv("SERVER_ENV", "development")
    
    is_prod = env.lower() == "production"

    app, socket = create_server()

    define_routes(app)
    define_socket_routes(socket)

    debug = False if is_prod else True
    host = "0.0.0.0" if is_prod else "127.0.0.1"

    socket.run(app, host=host, port=8000, debug=debug)
