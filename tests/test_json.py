import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper

    km = KeyMapper(json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc', 'test_json.json'), 'r').read()))
    print(km['web-app']['servlet'][0]['init-param'])
    print(km['web-app.servlet.0.init-param'])