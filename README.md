# TinyProtobuf

Tiny library for designing custom message formats. Messages are written as pure python scripts and compiled to c++ for usage.

## Example

Write some struct definitions in python. Add fields and vectors and then compile to header

```py
from compile import *
int32 = struct('Int32').add_field('data', int32_t)
int32_array = struct('Int32Array').add_vector('data', int32_t)

ns = namespace('std_msgs')
ns += int32
ns += int32_array
ns.compile('msg.h')
```

This message can then be used in c++. Set and get data fields

```cpp
std_msgs::Int32 i;
i.set_data(5);
std_msgs::Int32Array ia;
ia.set_data(std::vector<std::int32_t>{1, 2, 3});
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
