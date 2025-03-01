# JSON* is an extensible json module to serialize all objects!

`jsonstar` extends Python's standard JSON encoder and decoder to easily handle your custom types.

This means you won't have to transform your custom types into dictionaries with primitive types before encoding them to
JSON. And you won't have to parse back the encoded strings into your custom types after decoding them from JSON.

## How to install it?

```bash
pip install jsonstar
````

## How to start using it?

The `jsonstar` module provides the same API as the standard `json` module, so you can use it as a drop in replacement.

Simply change your import from `import json` to `import jsonstar as json` and you're good to go.

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
Your solution would include some transfomation of the `employee` instance and its attributes before encoding it to JSON.

That is where `jsonstar` shines by providing default encoder for common types like `pydantic.BaseModel`,
`decimal.Decimal`, `datetime.date` and `set`. And allowing you to easily add your own encoders.

```python
from jsonstar as json
print(json.dumps(employee))
# {"name": "John Doe", "salary": "1000.00", "birthday": "1990-01-01", "roles": ["A", "B", "C"]}
```

## What default encoders are provided?

By default, `jsonstar` provides encoders for the following types:

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

### Can `jsonstar` add more default encoders?

Yes. If you think that a default encoder for a common type is missing, please open an issue or a pull request.
See the *How to contribute* section for more details.

## How do I add my own encoder?

First you need to decide where you want your encoder to be available:

1. *Class default encoders* happen when your `MyEncoder` class inherits from `JSONEncoderStar` and you add encoders to it.
2. *Library-wide default encoder* are added directly to `JSONEncoderStar` class and is available everywhere in your project.

Also you have two types of encoders to choose from:

- *Typed encoders* are used to encode a specific type identified by `isinstance`.
- *Functional encoders* are used to encode an object based on arbitraty logic.

*Note:* From experience we find that *class encoders* are the most common use case.

### How to add class default encoders?

```python
import jsonstar as json
from decimal import Decimal
from datetime import date


# You can declare it on the special class attributes
class MyEncoder(json.JSONEncoderStar):
    _default_typed_encoders = {Decimal: lambda o: str(o.quantize(Decimal("1.00")))}

# Or you can register it after the class is declared
MyEncoder.register_default_encoder(lambda o: o.strftime("%Y-%m-%d"), date)
```

### How to add a library-wide default encoder?

```python
import jsonstar as json
from decimal import Decimal


def two_decimals_encoder(obj):
    """Encodes a decimal with only two decimal places."""
    return str(obj.quantize(Decimal("1.00")))


json.register_default_encoder(Decimal, two_decimals_encoder)
```

### How to add a typed encoder?

*Typed encoders* are specific to a type and it's inherited types.

When registering a typed encoder, you simply pass the encoder and the type to the chosen registration method.

When you add a typed encoder, `jsonstar` will check if any base class already has a registered encoder make sure the
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
- [Homepage](https://github.com/henriquebastos/python-jsonstar)
- [Repository](https://github.com/henriquebastos/python-jsonstar)
- [Documentation](https://github.com/henriquebastos/python-jsonstar)
