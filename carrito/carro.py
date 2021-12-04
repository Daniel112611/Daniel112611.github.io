class Carrito:
    def __init__(self, request):
        self.request = request
        self.request = request.session
        carrito = self.session.get("carrito")
