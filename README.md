# KeyMapper

**KeyMapper is a subclass of the dictionary class, which allows you to:**
- Assign keys and values dynamically 
- Choose what delimiter you want (default is dot-notation: .)
- Access all keys and values in a single key declaration regardless of type (list, tuple, set)
- Is treated as a dict type by default
- Initializes an empty dictionary, or accepts an existing dict upon class declaration
- Great for key iteration and loops
- KeyMapper functionality is not forced on you

## Installation
- You can install either via pypi:

        pip install keymapper

- Or, install it locally after the package has been unarchived:

        pip install -e /destination


## Examples

**Standard Dict:**

```python
from keymapper import KeyMapper

km_dict = KeyMapper()
print(km_dict)
# Prints: {} 

km_dict['key1'] = 'All the keys!'
print(km_dict)
# Prints: {'key1': 'All the keys!'}
```

**Nested Dict:**

```python
from keymapper import KeyMapper

my_dict = {'messages': {'message_1': 'Hey there!'}}
km_dict = KeyMapper(my_dict)

# Standard
print(km_dict['messages']['message_1'])  # Prints: 'Hey there!'

# KeyMapper
print(km_dict['messages.message_1'])  # Prints: 'Hey there!'
```

**Dict with iterables:**

```python
from keymapper import KeyMapper

my_dict = {
   'messages': {'message_1': 'Hey there!'}, 
   'objects': [{'obj1': 'Hi!'}], 
   'objects2': ({'obj2': 'There!'}), 
   'objects3': {'A', 'Peoples!', 'Friend?'}
}
km_dict = KeyMapper(my_dict)

# Standard
print(km_dict['objects'][1]['obj2'])  # Prints: 'There!'

# KeyMapper - does not care what type of iterable
print(km_dict['objects2.0.obj2'])  # Prints: 'There!'
print(km_dict['objects3.1'])  # Prints: 'Peoples!'
print(km_dict['objects.0.obj1'])  # Prints: 'Hi!'

# Or don't even declare the data type
print(km_dict['objects.1.obj2'])  # Prints: 'There!'
```

**Dict with different delimieter:**

```python
from keymapper import KeyMapper

my_dict = {'messages': {'message_1': 'Hey there!'}, 'objects': [{'obj1': 'Hi!'}, {'obj2': 'There!'}, {'obj3': 'Peoples!'}]}

km_dict = KeyMapper(my_dict, delimiter=',')

# Standard
print(km_dict['messages']['message_1'])  # Prints: 'Hey there!'

# KeyMapper with new delimeter
print(km_dict['messages,message_1'])  # Prints: 'Hey there!'
```

**Example**

```python
from keymapper import KeyMapper

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
```
