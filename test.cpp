#include <iostream>
#include "msg.h"

int main(void) {
  std_msgs::Int32 i;
  i.set_data(5);
  std::vector<char> is(i.size());
  i.serialize(is.data());
  std_msgs::Int32 i2;
  i2.deserialize(is.data(), is.size());
  std::cout << "i data = " << i.get_data() << std::endl << "i deser data = " << i2.get_data() << std::endl;

  std_msgs::Int32Array ia;
  std::vector<std::int32_t> arr{1, 2, 3};
  ia.move_data(std::move(arr));
  std::cout << "arr size after move = " << arr.size() << std::endl;
  const auto& rv = ia.get_data();
  std::cout << "i arr size = " << rv.size() << std::endl;
  for (const auto v : rv) {
    std::cout << "i arr elem " << v << std::endl;
  }
  std::vector<char> ias(ia.size());
  ia.serialize(ias.data());
  std_msgs::Int32Array ia2;
  ia2.deserialize(ias.data(), ias.size());
  const auto& rv2 = ia2.get_data();
  std::cout << "i deser arr size = " << rv2.size() << std::endl;
  for (const auto v : rv2) {
    std::cout << "i deser arr elem " << v << std::endl;
  }

  return 0;
}
