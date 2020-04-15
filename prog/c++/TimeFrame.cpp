#include "timeframe.h"

#include <iostream>

int main(int argc, char const *argv[]) {
  interval<int> i1(5, 10, 1, 1);
  interval<int> i2(0,5,1,0);
  interval<int> i3(4,7,0,0);
  // if(i1.have_intersect(i2)){
  //   i3 = i1.intersect(i2);
  //   std::cout << (i3.lower_inc ? "[" : "(" ) << i3.lower << ',' << i3.upper << (i3.upper_inc ? "]" : ")");
  //  }
  // else
  //   std::cout << "you done goofed" << '\n';

  interval<int> parr[] = {i1, i2};
  interval<int> qarr[] = {i3};
  po_set<int> p(parr, 2);
  po_set<int> q(qarr,1);
  po_set<int> intc = p.set_union(q);
  std::cout << p.to_string() << '\n';
  std::cout << q.to_string() << '\n';
  std::cout << intc.to_string() << '\n';
  intc.order();
  intc.clean();
  std::cout << intc.to_string() << '\n';

  return 0;
}
