import sys, os, datetime, json, gc

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper
    test_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc', 'test_json.json'), 'r')
    json_fmt = json.loads(test_file.read())

    dummy_dict = json_fmt
    start = datetime.datetime.now()
    print('Standard Dictionary: {}'.format(dummy_dict['web-app']['servlet'][0]['init-param']['maxUrlLength']))
    print('Time execution: {} \n\n###### \n '.format(datetime.datetime.now() - start))

    my_dict = json_fmt
    start = datetime.datetime.now()
    print('Standard Dictionary: {}'.format(my_dict['web-app']['servlet'][0]['init-param']['maxUrlLength']))
    print('Time execution: {} \n\n###### \n'.format(datetime.datetime.now() - start))

    km2 = KeyMapper(json_fmt)
    start = datetime.datetime.now()
    print('KeyMapper Single Key: {}'.format(km2['web-app.servlet.0.init-param.maxUrlLength']))
    print('Time execution: {} \n\n###### \n '.format(datetime.datetime.now() - start))

    km1 = KeyMapper(json_fmt)
    start = datetime.datetime.now()
    print('KeyMapper Standard Declaration: {}'.format(km1['web-app']['servlet'][0]['init-param']['maxUrlLength']))
    print('Time execution: {}'.format(datetime.datetime.now() - start))

    test_file.close()