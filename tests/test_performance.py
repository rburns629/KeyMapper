import sys, os, datetime, json, gc

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper

    km = KeyMapper(json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc', 'test_json.json'), 'r').read()))
    start = datetime.datetime.now()
    print('KeyMapper Standard Declaration: {}'.format(km['web-app']['servlet'][0]['init-param']['maxUrlLength']))
    print('Time execution: {}'.format(datetime.datetime.now() - start))

    my_dict = dict(json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc', 'test_json.json'), 'r').read()))
    start = datetime.datetime.now()
    print('Standard Dictionary: {}'.format(my_dict['web-app']['servlet'][0]['init-param']['maxUrlLength']))
    print('Time execution: {}'.format(datetime.datetime.now() - start))

    km = KeyMapper(json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc', 'test_json.json'), 'r').read()))
    start = datetime.datetime.now()
    print('KeyMapper Single Key: {}'.format(km['web-app.servlet.0.init-param.maxUrlLength']))
    print('Time execution: {}'.format(datetime.datetime.now() - start))