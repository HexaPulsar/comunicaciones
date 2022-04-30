
ind = input('input')

def state(cliente,solicitud):
    if ind == "::state":
        return solicitud.state()