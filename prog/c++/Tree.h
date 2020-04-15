#ifndef _TREE_H_
#define _TREE_H_

#include <string>

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
