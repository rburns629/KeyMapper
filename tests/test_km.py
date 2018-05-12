import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)).split('/tests')[0])

if __name__ == '__main__':
    from keymapper import KeyMapper

    mapper = KeyMapper()  # Initialize an empty dictionary

    # Test iteration support
    mapper['d'] = {}
    mapper['d.a'] = [{'d': 'f'}, {'c': 'e'}, {'d': 'c'}]
    print(mapper['d.a'])

    # What happens when you have an iterable...?
    print(mapper['d.a'][0]['d'])
    print(mapper['d.a.[0].d'])  # Can use: 0-9, [0-9], (0-9), {0-9}

    questions = ['What is your name: ', 'What is your email: ', 'What is your password: ', 'How many servers do you want to add: ', 'What is the ip: ', 'What is the port: ']
    keys = ['user.name', 'user.email', 'user.password', 'servers']
    config = {'user': {'name': '', 'email': '', 'password': ''}, 'servers': []}

    km_dict = KeyMapper(config)

    for i in range(len(questions)):
        if i < 3:
            km_dict[keys[i]] = input(questions[i])
        else:
            for r in range(int(input(questions[i]))):
                server_info = {'ip': '', 'port': ''}
                for i, k in enumerate(questions[4:]):
                    if i < 1:
                        server_info['ip'] = input(k)
                    else:
                        server_info['port'] = input(k)
                km_dict[keys[len(keys) - 1]].append(server_info)
            break
    print(km_dict)  # Prints: ... Well, whatever you entered as your input values! Try it if you don't believe me ;)
    for i in range(len(km_dict['servers'])):
        print(km_dict['servers.{}.ip'.format(i)])  # Prints the IP for each index iterated through