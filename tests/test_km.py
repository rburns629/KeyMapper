import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper
    
    km_dict = KeyMapper()  # Initialize an empty dictionary

    km_dict['d']    = {}
    km_dict['d.a']  = [{'d': 'f'}, {'c': 'e'}, {'d': 'c'}]
    km_dict['d.z']  = ({'r': 'j'}, {'g': 'y'}, {'v': 't'})

    km_dict['d.x']  = {1, 2, 33, 4}
    print(km_dict['d.a'])
    print(km_dict['d.a'][0]['d'])
    print(km_dict['d.a.0.d'])  # Can use: 0-9, [0-9], (0-9), {0-9}

    km_dict['d.a'].append({'d': 'f'})
    km_dict['d.a'].append('v')
    km_dict['d.a'].pop(1)
    km_dict['d.a'].remove('v')

    # Tuple
    try:
        km_dict['d.z'].pop(-1)
    except Exception as e:
        pass

    # Tuple
    try:
        km_dict['d.z'].add(7)
    except Exception as e:
        pass

    km_dict['d.x'].add('BAHHHH')

    km_dict['d.z']      = 'Getting rid of this tuple!'
    km_dict['d.a.0']    = 'fdsfds'

    print(km_dict)