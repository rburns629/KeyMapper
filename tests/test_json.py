import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper

    json_t_f    = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc', 'test_json.json'), 'r')
    json_read   = json.loads(json_t_f.read())
    km          = KeyMapper(json_read)

    print(km['web-app']['servlet'][0]['init-param'])
    print(km['web-app.servlet.0.init-param'])

    json_t_f.close()