from htmlmin.main import minify

from skybird import app, config

@app.after_request
def response_minify(response):
    """ Minify html response to decrease site traffic """
    if response.content_type == u'text/html; charset=utf-8':
        data = minify(response.get_data(as_text=True))
        response.set_data(data)
        return response
        
    return response
