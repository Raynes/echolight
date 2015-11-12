from echolight.config import EcholightConfig
import flask

app = flask.Flask('echolight')
conf = EcholightConfig()


def server():
    app.run('0.0.0.0', 8184, debug=True)


def _format_response(message):
    body = {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message
            },

            'shouldEndSession': True
        }
    }

    return flask.jsonify(**body)


def apply_preset(req):
    print(req)
    preset_name = req["intent"]["slots"]["PresetName"]["value"]
    preset = conf.presets.get(preset_name)
    if preset:
        conf.groups.get(preset['groups'][0]).hue = preset['hue']
    return _format_response("Switching...")


@app.route('/echolight', methods=['POST'])
def dispatch_request():
    body = flask.request.get_json()
    req = body['request']

    if req['type'] != 'IntentRequest':
        return 'nope', 400

    intent_handler = {
        'ApplyPreset': apply_preset,
    }.get(req['intent']['name'])

    if intent_handler:
        return intent_handler(req)

    return 'NO.', 400

if __name__ == '__main__':
    server()
