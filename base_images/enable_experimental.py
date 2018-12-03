import json
from os.path import expanduser


def main():
    fname = f'{expanduser("~")}/.docker/config.json'
    try:
        with open(fname, 'r') as f:
            content = f.read()
            config = json.loads(content or '{}')
    except FileNotFoundError:
        config = {}

    if 'experimental' in config.keys():
        return

    with open(fname, 'w') as f:
        config['experimental'] = 'enabled'
        json.dump(config, f, indent=4)


if __name__ == '__main__':
    main()
