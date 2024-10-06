class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            self.session["carro"] = {}
            carro = self.session["carro"]
        self.carro = carro
    
    def agregar(self, mensualidad):
        if str(mensualidad.id_mensualidad) not in self.carro.keys():
            self.carro[mensualidad.id_mensualidad] = {
                "id_mensualidad": mensualidad.id_mensualidad,
                "monto": mensualidad.monto_mensualidad,
                "cantidad": 1
            }

        self.guardar()
    
    def guardar(self):
        self.session["carro"] = self.carro
        self.session.modified = True
    
    def eliminar(self, mensualidad):
        id_mensualidad = str(mensualidad.id_mensualidad)
        if id_mensualidad in self.carro:
            del self.carro[id_mensualidad]
            self.guardar()
    
    def quitar(self, mensualidad):
        if str(mensualidad.id_mensualidad) in self.carro.keys():
            self.carro[mensualidad.id_mensualidad]["cantidad"] -= 1
            if self.carro[mensualidad.id_mensualidad]["cantidad"] < 1:
                self.eliminar(mensualidad)
            else:
                self.guardar()
    
    def limpiar(self):
        self.session["carro"] = {}
        self.session.modified = True
            