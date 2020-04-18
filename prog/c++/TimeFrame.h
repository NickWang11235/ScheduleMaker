#ifndef _TIMEFRAME_H_
#define _TIMEFRAME_H_

#include <string>
#include <map>
#include <assert.h>

#include "set.h"
#include "interval.h"

struct integer;
struct week_day;
struct class_time;

class timeframe{
private:
  std::map<week_day, po_set<integer>> _schedule;
  bool have_conflict(const class_time& time);
public:
  timeframe();
  bool add_to_schedule(const class_time& time);
  bool add_to_schedule(const char day, const int begin, const int end);
  std::map<week_day, po_set<integer>> schedule() const;
  std::string to_string() const;
};

#endif
