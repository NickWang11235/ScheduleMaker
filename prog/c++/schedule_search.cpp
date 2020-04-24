#include <vector>
#include "schedule_search.h"

struct course{
  int _id;
  std::string _days;
  std::vector<class_time> _time;
  int _space;
  int _max;
  std::vector<course>*;
  course(const int& id, const std::string& days, const std::vector<class_time>& time, const int& space, const int& max){
    _id = id;
    _days = days;
    _time = time;
    _space = space;
    _max = max;
  }
}

course_tree::course_tree(const std::string& name, const double& units, const grading& option);{
    _name = name;
    _units = units;
    _option = option;
}

void course_tree::set_name(const std::string& name){
    _name = name;
}

void course_tree::set_units(const double& units){
  _units = units;
}

void course_tree::set_option(const grading& option){
  _option = option;
}

std::void course_tree::add_lecture(const course& lecture){
  _lecture.push_back(lecture);
}

std::string course_tree::name() const{
  return _name;
}

double course_tree::units() const{
  return _units;
}
grading course_tree::option() const{
  return option;
}

std::vector<course> course_tree::lecture() const{
  return lecture;
}
