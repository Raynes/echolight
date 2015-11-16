# Echolight

Echolight is a Python 3 flask app for controlling Phillips Hue light groups
with Amazon Echo commands.

## Usage

Clone the repository and create a virtual environment:

```
$ pyvenv .env
$ . .env/bin/activate
$ pip install --editable .
$ python -m echolight
```

You can turn debug mode on by passing a `-d` option, and change the default
port (`8184`) with `-p`.

## Config

Echolight works on presets, so you'll want a config file that looks like this:

**config.json**

```json
{
  "username": "REDACTED",
  "ip": "192.168.1.237",
  "presets": {
    "sunset": {
      "groups": ["Apartment"],
      "hue": 9646,
      "brightness": 180
    },
    "halsey": {
      "groups": ["Apartment"],
      "hue": 46920
    },
    "hell": {
      "groups": ["Apartment"],
      "hue": 0
    }
  }
}
```

This is my own personal config, so you'll probably want to tweak it. For
example, some people don't much like their apartment to have a 'hell' setting.


## Reloading Configuration

You can reload configuration at runtime by asking it to "reload config" or
"reload configuration". This'll cause it to re-read `config.json`. It
will not automatically update the current preset, you'll have to tell it
to set it again to get the changes reflected in reality.
