int8_t    = 'std::int8_t'
uint8_t   = 'std::uint8_t'
int16_t   = 'std::int16_t'
uint16_t  = 'std::uint16_t'
int32_t   = 'std::int32_t'
uint32_t  = 'std::int64_t'
int64_t   = 'std::int64_t'
uint64_t  = 'std::uint64_t'
float32_t = 'float'
float64_t = 'double'
bool_t    = uint8_t

class struct(object):
    def __init__(self, name):
        self.name = name
        self.fields = {}
        self.vectors = {}
    def add_field(self, name, type):
        self.fields[name] = type
        return self
    def add_vector(self, name, type):
        self.vectors[name] = type
        return self
    def compile(self):
        rv = 'class {} {{\npublic:\n'.format(self.name)
        rv += """
inline std::size_t size() {
  std::size_t total_size{HEADER_SIZE};
"""
        for key, value in self.vectors.items():
            rv += '  total_size += {}.size() * sizeof({});\n'.format(key, value)
        rv += '  return total_size;\n}\n\n'
        for key, value in self.fields.items():
            rv += 'inline {} get_{}() {{ return header_.{}; }}\n'.format(value, key, key)
            rv += 'inline void set_{}(const {}& i) {{ header_.{} = i; }}\n'.format(key, value, key)
        for key, value in self.vectors.items():
            rv += 'inline std::vector<{}> get_{}() {{ return {}; }}\n'.format(value, key, key)
            rv += 'inline void set_{}(const std::vector<{}>& i) {{ {} = i; header_.{}_size = i.size(); }}\n'.format(key, value, key, key)
        rv += """
inline void serialize(char* buffer) {
  std::size_t index = 0;
  std::size_t next_size = HEADER_SIZE;
  std::memcpy(buffer + index, &header_, next_size);
"""
        for key, value in self.vectors.items():
            rv += '  index += next_size;\n'
            rv += '  next_size = {}.size() * sizeof({});\n'.format(key, value)
            rv += '  std::memcpy(buffer + index, {}.data(), next_size);\n'.format(key)
        rv += '}\n'
        rv += """
inline void deserialize(const char* buffer, const size_t buffer_size) {
  std::size_t index = 0;
  std::size_t next_size = HEADER_SIZE;
  assert(index + next_size <= buffer_size);
  std::memcpy(&header_, buffer, next_size);
"""
        for key, value in self.vectors.items():
            rv += '  index += next_size;\n'
            rv += '  next_size = header_.{}_size * sizeof({});\n'.format(key, value)
            rv += '  {}.resize(header_.{}_size);\n'.format(key, key)
            rv += '  assert(index + next_size <= buffer_size);\n'
            rv += '  std::memcpy({}.data(), buffer + index, next_size);\n'.format(key)
        rv += '}\n\n'
        rv += 'private:\n\n'
        rv += 'struct __header__ {\n'
        for key, value in self.fields.items():
            rv += '  {} {};\n'.format(value, key)
        for key, _ in self.vectors.items():
            rv += '  std::size_t {}_size;\n'.format(key)
        rv += '};\n'
        rv += '__header__ header_;\nstatic const std::size_t HEADER_SIZE{sizeof(__header__)};\n'
        for key, value in self.vectors.items():
            rv += 'std::vector<{}> {};\n'.format(value, key)
        rv += '\n};\n'
        return rv
    def __repr__(self):
        return self.compile()

class namespace(object):
    def __init__(self, name):
        self.msgs = []
        self.name = name
    def __iadd__(self, m):
        self.msgs.append(m)
        return self
    def compile(self, filename):
        rv = '#include <cassert>\n#include <cstdint>\n#include <vector>\nnamespace {} {{\n\n'.format(self.name)
        for msg in self.msgs:
            rv += msg.compile()
            rv += '\n'
        rv += '}\n'
        with open(filename, 'w') as fi:
            fi.write(rv)
