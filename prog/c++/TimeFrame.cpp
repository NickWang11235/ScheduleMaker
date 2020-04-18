#include "timeframe.h"

struct integer{
  int num;
  integer(){}
  integer(int num){this->num = num;}
  bool operator==(const integer& o) const{return num == o.num;}
  bool operator<(const integer& o) const{return num < o.num;}
  bool operator>(const integer& o) const{return num > o.num;}
  std::string to_string() const {return std::to_string(num);}
};

struct week_day{
  char day = ' ';

  week_day(){}
  week_day(const char day){
    if(day == 0)
      this->day=0;
    else{
      assert(is_day_of_week(day));
      this->day = toupper(day);
    }
  }

  bool operator==(const week_day& o) const{return day == o.day;}
  bool operator<(const week_day& o) const{
    char days[] = {'M','T','W','R','F','S','U'};
    int p1 = 0, p2 = 0;
    for(int i = 0; i < 7; i++){
      if(days[i] == day)
        p1 = i;
      if(days[i] == o.day)
        p2 = i;
    }
    return p1 < p2;
  }
  bool operator>(const week_day& o) const{return !(*this < o || *this == o);}

  static bool is_day_of_week(const char day){
    switch (tolower(day)) {
      case 'm': case 't': case 'w': case 'r':
      case 'f': case 's': case 'u':
        return true;
      default:
        return false;
    }
  }

  std::string to_string() const {return std::string(1,day);}

};

struct class_time{
  week_day day;
  interval<integer> hour;
  class_time(const week_day& day, const interval<integer>& hour){
    this->day = day;
    this->hour = hour;
  }
  class_time(const char day, const int begin, const int end){
    assert(begin < end);
    this->day = week_day(day);
    this->hour = interval<integer>(integer(begin), integer(end), 1, 0);
  }
};

timeframe::timeframe(){
    _schedule.insert({week_day('m'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
    _schedule.insert({week_day('t'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
    _schedule.insert({week_day('w'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
    _schedule.insert({week_day('r'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
    _schedule.insert({week_day('f'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
    _schedule.insert({week_day('s'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
    _schedule.insert({week_day('u'), po_set<integer>(interval<integer>(integer(0),integer(0),0,0))});
}

bool timeframe::add_to_schedule(const class_time& time){
  if(have_conflict(time))
    return false;
  _schedule[time.day] = _schedule[time.day].set_union(po_set<integer>(time.hour));
  return true;
}

bool timeframe::add_to_schedule(const char dayc, const int begin, const int end){
  return add_to_schedule(class_time(dayc,begin,end));
}

bool timeframe::have_conflict(const class_time& time){
  if(_schedule[time.day].set_intersect(po_set<integer>(time.hour)).is_empty())
    return false;
  return true;
}

std::map<week_day, po_set<integer>> timeframe::schedule() const{
  return _schedule;
}

std::string timeframe::to_string() const{
  std::string str = "Hr M T W R F S U\n";
  for(int i = 0; i < 24; i++){
    std::string temp = std::to_string(i);
    temp.append(3-temp.length(), ' ');
    for(auto it = _schedule.begin(); it != _schedule.end();it++){
      if(it->second.set_intersect(po_set<integer>(interval<integer>(integer(100*i),integer(100*(i+1)),1,0))).is_empty())
        temp += "--";
      else
        temp += "X-";
    }
    str += temp + "\n";
  }
  return str;
}
