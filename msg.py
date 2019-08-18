from compile import *

int32 = struct('Int32') \
    .add_field('data', int32_t) \
    .add_field('data2', int32_t) \
    .add_field('data3', int32_t)

int32_array = struct('Int32Array') \
    .add_vector('data', int32_t, range(10)) \
    .add_field('data2', int32_t) \
    .add_vector('data3', int32_t)

ns = namespace('std_msgs')
ns += int32
ns += int32_array
ns.compile('msg.h')
