import argparse
from echolight.config import EcholightConfig
import flask

app = flask.Flask('echolight')
conf = EcholightConfig()


def server(port, debug):
    app.run('0.0.0.0', port, debug)


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
    preset_name = req["intent"]["slots"]["PresetName"]["value"].lower()
    preset = conf.presets.get(preset_name)
    if preset:
        for group_name in preset['groups']:
            group = conf.groups.get(group_name)
            if group:
                group.on = True
                group.hue = preset['hue']
                group.brightness = preset.get('brightness', 254)
                group.saturation = preset.get('saturation', 254)
            else:
                return _format_response(
                    "Failed to find group {}".format(group_name)
                )
        return _format_response("Switched to {}".format(preset_name))
    else:
        return _format_response("Preset not found")


def reload_config(req):
    try:
        conf.load_config()
        return _format_response("Reloaded configuration")
    except Exception as e:
        print(e.message)
        return _format_response("Failed to reload configuration")


@app.route('/echolight', methods=['POST'])
def dispatch_request():
    body = flask.request.get_json()
    req = body['request']

    if req['type'] != 'IntentRequest':
        return 'nope', 400

    intent_handler = {
        'ApplyPreset': apply_preset,
        'ReloadConfig': reload_config
    }.get(req['intent']['name'])

    if intent_handler:
        return intent_handler(req)

    return 'NO.', 400

if __name__ == '__main__':
    description = "Presets for hue light groups, controlled via Amazon Echo"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--port',
                        type=int,
                        default=8184,
                        help="Port to run the server on.")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    server(args.port, args.debug)
