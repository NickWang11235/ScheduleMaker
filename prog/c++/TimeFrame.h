#ifndef _TIMEFRAME_H_
#define _TIMEFRAME_H_

#include <vector>
#include <algorithm>
#include <string>

/**
 * A continous interval, closed or open, that is bounded by a lower and an upper value
 */
template <class T>
struct interval{
  T lower;
  T upper;
  bool lower_inc;
  bool upper_inc;


  interval() :  lower_inc(true), upper_inc(true){}

  /**
   * Constructs an interval, asserts the lower bound is smaller than or equal to
   * the upper bound
   *
   * @param l lower bound
   * @param u upper bound
   * @param li inclusivity, lower bound
   * @param ui inclusivity, upper bound
   */
  interval(T l, T u, bool li, bool ui) : lower(l), upper(u), lower_inc(li), upper_inc(ui){
    if (u < l || (lower == upper && !(lower_inc && upper_inc))){
      lower = 0; upper = 0; lower_inc = 0; upper_inc = 0;
    }
  }

  /**
   * Checks if a value is bounded by the interval
   *
   * @param element the value to be checked
   * @return
   */
  bool contains(const T element) const{
    return (element > lower && element < upper)
        || (element == lower && lower_inc)
        || (element == upper && upper_inc);
  }

  bool is_empty() const{
    return lower == upper && !(lower_inc && upper_inc);
  }

  bool operator==(const interval& o) const{
    return lower == o.lower && upper == o.upper
        && lower_inc == o.lower_inc && upper_inc == o.upper_inc;
  }

  /**
   * Finds the intersect of 2 intervals
   *
   * @param intv
   * @return
   */
  interval intv_intersect(const interval& intv) const{
    T i_lower = std::max(lower, intv.lower);
    T i_upper = std::min(upper, intv.upper);
    return interval(i_lower, i_upper, contains(i_lower) && intv.contains(i_lower),
                                      contains(i_upper) && intv.contains(i_upper));
  }

  /**
   * Finds the union of 2 intervals if the resulting interval is continous
   *
   * @param intv
   * @return
   */
  std::vector<interval<T>> intv_union(const interval& intv) const{
    std::vector<interval<T>> v;
    T i_lower = std::min(lower, intv.lower);
    T i_upper = std::max(upper, intv.upper);
    if(*this == intv){
      v.push_back(intv);
      return v;
    }
    if(contains(intv.lower) || intv.contains(lower)){
      v.push_back(interval(i_lower, i_upper, contains(i_lower) || intv.contains(i_lower),
                                             contains(i_upper) || intv.contains(i_upper)));
      return v;
    }
    v.push_back(*this);
    v.push_back(intv);
    return v;
  }

  std::vector<interval<T>> intv_difference(const interval& intv) const{
    interval i = intv_intersect(intv);
    std::vector<interval<T>> v;
    v.push_back(interval(lower, i.lower, lower_inc, !i.lower_inc));
    v.push_back(interval(i.upper, upper, !i.upper_inc, upper_inc));
    return v;
  }

  /**
   * Returns a string representation of the interval
   *
   * @return
   */
  std::string to_string() const{
    return (lower_inc ? "[" : "(" ) + std::to_string(lower) + ","
                                    + std::to_string(upper) + (upper_inc ? "]" : ")");
  }
};

/**
 * A collection of intervals
 */
template <class T>
class po_set{
private:
  std::vector<interval<T>> _intervals;
public:

  po_set(){
    std::vector<interval<T>> v;
    _intervals = v;
  }

  po_set(interval<T> intv){
    _intervals.push_back(intv);
  }

  po_set(std::vector<interval<T>> intv){
    _intervals = intv;
  }

  /**
   * Constructs a poset with an array
   *
   * @param arr
   * @param size
   * @return
   */
  po_set(interval<T>* arr, int size){
    std::vector<interval<T>> v;
    for(int i = 0; i < size; i++)
      v.push_back(arr[i]);
    _intervals = v;
    clean();
  }

  bool is_empty() const{
    if(_intervals.empty())
      return true;
    for(int i = 0; i < _intervals.size(); i++)
      if(!_intervals.at(i).is_empty())
        return false;
    return true;
  }

  void clean(){
    order();
    set_family_union();
    int i = 0;
  }

  /**
   * Order the elements in the collection
   */
  void order(){
    std::sort(_intervals.begin(), _intervals.end(),
             [](const interval<T> a, const interval<T> b) -> bool{ return a.lower < b.lower; });
  }

  /**
   * Performs a union over the collection of sets
   */
  void set_family_union(){
    int i = 0;
    while(i < _intervals.size()-1){
      if(_intervals.at(i).is_empty()){
        _intervals.erase(_intervals.begin()+i);
        continue;
      }
      std::vector<interval<T>> v = _intervals.at(i).intv_union(_intervals.at(i+1));
      if(v.size() == 2){
        i++;
        continue;
      }
      _intervals.at(i) = v.at(0);
      _intervals.erase(_intervals.begin()+i+1);
    }
  }

  /**
   * Finds the intersect between 2 posets
   *
   * @param s
   * @return
   */
  po_set set_intersect(const po_set<T>& s) const{
    std::vector<interval<T>> new_intervals;
    for(int i = 0; i < _intervals.size(); i++)
      for(int j = 0; j < s._intervals.size(); j++)
          new_intervals.push_back(_intervals.at(i).intv_intersect(s._intervals.at(j)));
    po_set p(new_intervals);
    return p;
  }

  static void push_back_all(std::vector<interval<T>>& v1, const std::vector<interval<T>>& v2){
    for(int i = 0; i < v2.size(); i++)
      v1.push_back(v2.at(i));
  }
  /**
   * Finds the union between 2 posets
   *
   * @param s
   * @return
   */
  po_set set_union(const po_set<T>& s) const{
    if(is_empty())
      return s;
    std::vector<interval<T>> new_intervals, temp;
    for(int i = 0; i < _intervals.size(); i++)
      for(int j = 0; j < s._intervals.size(); j++)
        push_back_all(new_intervals, _intervals.at(i).intv_union(s._intervals.at(j)));

    po_set p(new_intervals);
    return p;
  }

  /**
   * Finds the difference of this - s
   *
   * @param s
   * @return
   */
  po_set set_difference(const po_set<T>& s) const{
    po_set<T> u;
    std::vector<interval<T>> temp;
    for(int i = 0; i < _intervals.size(); i++){
      po_set<T> p;
      for(int j = 0; j < s._intervals.size(); j++){
        temp = _intervals.at(i).intv_difference(s._intervals.at(j));
        if(p.is_empty()){
          p = po_set<T>(temp);
          continue;
        }
        p = p.set_intersect(po_set<T>(temp));
      }
      u = u.set_union(p);
    }
    return u;
  }

  /**
   * Finds the complement of this given universe u
   *
   * @param u
   * @return
   */
  po_set set_complement(const po_set<T>& u) const{
    return u.set_difference(*this);
  }

  /**
   * Returns a string representation of the poset
   *
   * @return
   */
  std::string to_string() const{
    std::string str = "";
    for(int i = 0; i < _intervals.size(); i++){
      str += _intervals.at(i).to_string();
      if(i < _intervals.size() - 1)
        str += "U";
    }
    return str;
  }
};

#endif
