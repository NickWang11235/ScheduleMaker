#include <vector>
#include "schedule_search.h"

struct course{
  int id;
  std::string days;
  class_time time;
  int space;
  int max;
  vector<course>;
  course(int id, std::string days, class_time time, int space, int max){
    this->id = id;
    this->days = days;
    this->time = time;
    this->space = space;
    this->max = max;
  }
}
