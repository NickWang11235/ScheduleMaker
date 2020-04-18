#ifndef _SCHEDULE_SEARCH_H_
#define _SCHEDULE_SEARCH_H_

#include <string>
#include <vector>

#include "timeframe.h"

struct course;

enum grading{Optional, PNP, Letter};

class course_tree{
private:
  std::string _name;
  double _units;
  grading _option;
  std::vector<course> _lecture;
public:
  tree(std::string name, double units, grading option);

  void set_name(const std::string name);
  void set_units(const double units);
  void set_option(const grading option);
  void add_lecture(const course lecture);

  std::string name() const;
  double units() const;
  grading option() const;
  std::vector<course> lecture() const;
};

#endif
