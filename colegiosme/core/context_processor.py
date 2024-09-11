def TotalVenta(request):
    total=0
    if request.user.is_authenticated:
        if "carro" in request.session.keys():
            for key, value in request.session["carro"].items():
                total+=int(value["monto"])
    
    return {"Total":total}