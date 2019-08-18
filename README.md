# TinyProtobuf

Tiny library for designing custom message formats. Messages are written as pure python scripts and compiled to c++ for usage.

## Example

Write some struct definitions in python. Add fields and vectors and then compile to header

```py
from compile import *
int32 = struct('Int32') \
  .add_field('data', int32_t, bitfield=4)
int32_array = struct('Int32Array') \
  .add_vector('data', int32_t, default_value=range(10))

ns = namespace('std_msgs')
ns += int32
ns += int32_array
ns.compile('msg.h')
```

This message can then be used in c++. Set, get, and move data into message fields

```cpp
std_msgs::Int32 i;
i.set_data(5);

std_msgs::Int32Array ia;
std::vector<std::int32_t> arr{1, 2, 3};
ia.move_data(std::move(arr));
const auto& rv = ia.get_data();
```

To serialize a message into a byte array

```cpp
std_msgs::Int32 msg;
std::vector<char> msg_array(msg.size());
msg.serialize(msg_array.data());
```

To deserialize a message from a byte array

```cpp
std_msgs::Int32 msg;
msg.deserialize(msg_array.data(), msg_array.size());
```

## Features

- Namespaces
- All numeric types, bool, vector's
- Default values
- Bitfields (without default value until c++20 I hear)
- Ordered fields for backwards compatibility

## TODO

- Composite types
- Enums, Unions
- Script Includes
- Msg unique id's
