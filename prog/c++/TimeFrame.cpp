#include "timeframe.h"

#include <iostream>

int main(int argc, char const *argv[]) {
  interval<int> i1(0, 5, 1, 1);
  interval<int> i2(8,34,1,0);
  interval<int> i3(50,100,1,1);
  interval<int> ia(10,20,1,1);
  interval<int> ib(40,90,1,1);
  interval<int> ic(0,100,0,0);


  interval<int> parr[] = {i1, i2, i3};
  interval<int> qarr[] = {ia, ib};
  po_set<int> p(parr, 3);
  po_set<int> q(qarr,2);


  std::cout << p.to_string() << '\n';
  std::cout << q.to_string() << '\n';
  po_set<int> intc(p.set_complement(po_set<int>(ic)));
  intc.clean();
  std::cout << intc.to_string() << '\n';

  return 0;
}
