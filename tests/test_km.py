import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper
    
    km_dict = KeyMapper()  # Initialize an empty dictionary

    km_dict['d'] = {}
    km_dict['d.a'] = [{'d': 'f'}, {'c': 'e'}, {'d': 'c'}]
    print(km_dict['d.a'])

    print(km_dict['d.a'][0]['d'])
    print(km_dict['d.a.[0].d'])  # Can use: 0-9, [0-9], (0-9), {0-9}