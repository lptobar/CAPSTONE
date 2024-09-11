class Carro:
    def __init__(self, request):
        self.request=request
        self.session=request.session
        carro=self.session.get("carro")
        if not carro:
            self.session["carro"]={}
            carro=self.session["carro"]
        self.carro=carro
    
    def Agregar(self,Mensualidad):
        if str(Mensualidad.id_mensualidad) not in self.carro.keys():
            self.carro[Mensualidad.id_mensualidad]={
                "id_mensualidad" : Mensualidad.id_mensualidad,
                "monto":Mensualidad.monto_mensualidad,
                "cantidad":1
            }
        self.Guardar()
    
    def Guardar(self):
        self.session["carro"]=self.carro
        self.session.modified=True
    
    def Eliminar(self,Mensualidad):
        id_mensualidad=str(Mensualidad.id_mensualidad)
        if id_mensualidad in self.carro:
            del self.carro[id_mensualidad]
            self.Guardar()
    
    def Quitar(self, Mensualidad):
        if str(Mensualidad.id_mensualidad) in self.carro.keys():
            self.carro[Mensualidad.id_mensualidad]["cantidad"]-=1
            if self.carro[Mensualidad.id_mensualidad]["cantidad"]<1:
                self.Eliminar(Mensualidad)
            else:
                self.Guardar()
    
    def Limpiar(self):
        self.session["carro"]={}
        self.session.modified=True
            