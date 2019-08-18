#include <cassert>
#include <cstdint>
#include <vector>
namespace std_msgs {

class Int32 {
public:

inline std::size_t size() const {
  std::size_t total_size{HEADER_SIZE};
  return total_size;
}

inline std::int32_t get_data() const { return header_.data; }
inline void set_data(const std::int32_t& i) { header_.data = i; }
inline void move_data(std::int32_t&& i) { header_.data = std::move(i); }

inline void serialize(char* buffer) const {
  std::size_t index = 0;
  std::size_t next_size = HEADER_SIZE;
  std::memcpy(buffer + index, &header_, next_size);
}

inline void deserialize(const char* buffer, const size_t buffer_size) {
  std::size_t index = 0;
  std::size_t next_size = HEADER_SIZE;
  assert(index + next_size <= buffer_size);
  std::memcpy(&header_, buffer, next_size);
}

private:

struct __header__ {
  std::int32_t data{0};
};
__header__ header_;
static const std::size_t HEADER_SIZE{sizeof(__header__)};

};

class Int32Array {
public:

inline std::size_t size() const {
  std::size_t total_size{HEADER_SIZE};
  total_size += data.size() * sizeof(std::int32_t);
  return total_size;
}

inline std::vector<std::int32_t> get_data() const { return data; }
inline void set_data(const std::vector<std::int32_t>& i) { header_.data_size = i.size(); data = i; }
inline void move_data(std::vector<std::int32_t>&& i) { header_.data_size = i.size(); data = std::move(i); }

inline void serialize(char* buffer) const {
  std::size_t index = 0;
  std::size_t next_size = HEADER_SIZE;
  std::memcpy(buffer + index, &header_, next_size);
  index += next_size;
  next_size = data.size() * sizeof(std::int32_t);
  std::memcpy(buffer + index, data.data(), next_size);
}

inline void deserialize(const char* buffer, const size_t buffer_size) {
  std::size_t index = 0;
  std::size_t next_size = HEADER_SIZE;
  assert(index + next_size <= buffer_size);
  std::memcpy(&header_, buffer, next_size);
  index += next_size;
  next_size = header_.data_size * sizeof(std::int32_t);
  data.resize(header_.data_size);
  assert(index + next_size <= buffer_size);
  std::memcpy(data.data(), buffer + index, next_size);
}

private:

struct __header__ {
  std::size_t data_size;
};
__header__ header_;
static const std::size_t HEADER_SIZE{sizeof(__header__)};
std::vector<std::int32_t> data{};

};

}
