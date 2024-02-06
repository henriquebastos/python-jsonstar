# JSONPlus: Extensible json encoder to serialize your custom types.

JSONPlus extends Python's standard JSON encoder and decoder to easily handle your custom types.

This means you won't have to transform your custom types into dictionaries with primitive types before encoding them to 
JSON. And you won't have to parse back the encoded strings into your custom types after decoding them from JSON.

## How to install it?

```bash
pip install jsonplus
````

## How to start using it?

The `jsonplus` module provides the same API as the standard `json` module, so you can use it as a drop in replacement.

Simply change your import from `import json` to `import jsonplus as json` and you're good to go.

## Why use it?

Consider you have a pydantic `Employee` class that you want to serialize to JSON.

```python
from decimal import Decimal
from datetime import date
from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    salary: Decimal
    birthday: date
    roles: set

employee = Employee(
    name="John Doe",
    salary=Decimal("1000.00"),
    birthday=date(1990, 1, 1),
    roles={"A", "B", "C"},
)    
```

The standard `json` module can't serialize the `employee` instance, requiring you to call its `dict` method.
This will not sufice, because the standard `json` module don't know how to encode `Decimal`, `date` and `set`.
Your solution would include some trasnfomation of the `employee` instance and its attributes before encoding it to JSON.

That is where `jsonplus` shines by providing default encoder for common types like `pydantic.BaseModel`, 
`decimal.Decimal`, `datetime.date` and `set`. And allowing you to easily add your own encoders.

```python
from jsonplus as json
print(json.dumps(employee))
# {"name": "John Doe", "salary": "1000.00", "birthday": "1990-01-01", "roles": ["A", "B", "C"]}
```

## What default encoders are provided?

By default, `jsonplus` provides encoders for the following types:

- `attrs` classes
- `dataclasses.dataclass` classes
- `datetime.date`
- `datetime.datetime`
- `datetime.time`
- `datetime.timedelta`
- `decimal.Decimal`
- `frozenset`
- `pydantic.BaseModel`
- `set`
- `uuid.UUID`

### Configurable default encoders

For some complex types like Django Models, an opinionated default encoder would not work for everyone.

This is why instead of providing a default encoder for Django Models, `jsonplus` provides you a configurable 
encoder class to allow you to define the desired encoding behavior.

```python
import jsonplus as json
from jsonplus import DjangoModelEncoder

json.register_default_encoder(Model, DjangoModelEncoder(exclude=[DjangoModelEncoder.RELATIONSHIPS]))
```

The above code will register a default encoder for the `Model` class that will return all fields, excluding 
relationships.

### Can `jsonplus` add more default encoders?

Yes. If you think that a default encoder for a common type is missing, please open an issue or a pull request. 
See the *How to contribute* section for more details.
 
## How do I add my own encoder?

First you need to decide if you want your encoder to be available everywhere on your project or just for a specific 
code block.

- *Default encoders* are globally available and will be used anywhere in your project.
- *Instance encoders* are available only for the `JSONEncoder` instance that you register them.

Also you have two types of encoders to choose from:

- *Typed encoders* are used to encode a specific type identified by `isinstance`.
- *Functional encoders* are used to encode an object based on arbitraty logic.

### How to add a default encoder?

To add a default encoder use the `register_default_encoder` function on the `jsonplus` module.

```python
import jsonplus as json
from decimal import Decimal


def two_decimals_encoder(obj):
    """Encodes a decimal with only two decimal places."""
    return str(obj.quantize(Decimal("1.00")))


json.register_default_encoder(Decimal, two_decimals_encoder)
```

### How to add an instance encoder?

An instance encoder can be added in three ways:

1. Using the `register` method on the `JSONEncoder` instance.
2. Passing the encoder to the `JSONEncoder` initialization.
3. Passing the encoder to the `dumps` function.

```python
import jsonplus as json
from decimal import Decimal


def two_decimals_encoder(obj):
    """Encodes a decimal with only two decimal places."""
    return str(obj.quantize(Decimal("1.00")))

# 1. Using the `register` method on the `JSONEncoder` instance.
encoder1 = json.JSONEncoder()
encoder1.register(two_decimals_encoder, Decimal)

# 2. Passing the encoder to the `JSONEncoder` initialization.
encoder2 = json.JSONEncoder(typed_encoders={Decimal: two_decimals_encoder})


# 3. Passing the encoder to the `dumps` function.
print(json.dumps(data, cls={Decimal: two_decimas_encoder}))
```

### How to add a typed encoder?

*Typed encoders* are specific to a type and it's inherited types.

When registering a typed encoder, you simply pass the encoder and the type to the chosen registration method.

When you add a typed encoder, `jsonplus` will check if any base class already has a registered encoder make sure the 
more generic encoder is used last, respecting Python's Method Resolution Order (MRO).


### How to add a functional encoder?

*Functional encoders* are used to encode an object based on arbitraty logic and not specific to a type.

To register a functional encoder, you simply pass the encoder to the chosen registration method omiting the type.

All functional encoders are called only for objects that do not have a registered typed encoder.


## Contributing
Pull requests are welcome and must have associated tests.

For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
Henrique Bastos <henrique@bastos.net>

## Project links
- [Homepage](https://github.com/henriquebastos/python-jsonplus)
- [Repository](https://github.com/henriquebastos/python-jsonplus)
- [Documentation](https://github.com/henriquebastos/python-jsonplus)
