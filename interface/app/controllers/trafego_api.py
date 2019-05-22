from app import app

@app.route('/teste', defaults = {'var': 'tchau'})
@app.route('/teste/<var>')
def teste(var):
    if var == 'oi':
        return "kkkkkk"
    elif var == 'tchau':
        return ":((("

    return "oops"
