#ifndef _SCHEDULE_SEARCH_H_
#define _SCHEDULE_SEARCH_H_

#include <string>

#include "timeframe.h"

struct course;

enum grading{Optional, PNP, Letter};

class tree{
private:
  std::string _name;
  int units;
  grading grade;
  course* lecture;

};

#endif
