#ifndef _TIMEFRAME_H_
#define _TIMEFRAME_H_

#include <iostream>
#include <assert.h>
#include <vector>
#include <algorithm>
using namespace std;

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
    assert(l <= u);
  }

  /**
   * Checks if a value is bounded by the interval
   *
   * @param element the value to be checked
   * @return
   */
  bool contains(T element){
    return (element > lower && element < upper)
        || (element == lower && lower_inc)
        || (element == upper && upper_inc);
  }

  /**
   * Checks if 2 intervals have an intersect
   *
   * @param intv
   * @return
   */
  bool have_intersect(interval intv){
    T l = std::max(lower, intv.lower);
    T u = std::min(upper, intv.upper);
    return l == u ? (lower < i.lower ? intv.lower_inc : lower_inc) &&
                    (upper > i.upper ? intv.upper_inc : upper_inc)
                  : l < u;
  }

  /**
   * Finds the intersect of 2 intervals
   *
   * @param intv
   * @return
   */
  interval intv_intersect(interval intv){
    assert(have_intersect(intv));
    T i_lower = std::max(lower, intv.lower);
    T i_upper = std::min(upper, intv.upper);
    return interval(i_lower, i_upper, contains(i_lower) && intv.contains(i_lower),
                                      contains(i_upper) && intv.contains(i_upper));
  }

  /**
   * Checks if 2 intervals have an union. Though mathematically the union will
   * always exist, the function checks if the resulting interval is continous
   *
   * @param intv
   * @return
   */
  bool have_union(interval intv){
    return have_intersect(intv);
  }

  /**
   * Finds the union of 2 intervals if the resulting interval is continous
   *
   * @param intv
   * @return
   */
  interval intv_union(interval intv){
    assert(have_union(intv));
    T i_lower = std::min(lower, intv.lower);
    T i_upper = std::max(upper, intv.upper);
    return interval(i_lower, i_upper, contains(i_lower) || intv.contains(i_lower),
                                      contains(i_upper) || intv.contains(i_upper));
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
  vector<interval<T>> _intervals;
public:

  po_set(vector<interval<T>>& intv){_intervals = intv;}

  /**
   * Constructs a poset with an array
   *
   * @param arr
   * @param size
   * @return
   */
  po_set(interval<T>* arr, int size){
    vector<interval<T>> v;
    for(int i = 0; i < size; i++)
      v.push_back(arr[i]);
    _intervals = v;
  }

  /**
   * Order the elements in the collection
   */
  void order(){
    std::sort(_intervals.begin(), _intervals.end(),
             [](const interval<T> a, const interval<T> b) -> bool{ return a.lower < b.lower; });
  }

  /**
   * Combines intervals in the collection that are not disjoint
   */
  void clean(){
    int i = 0;
    while(i < _intervals.size()-1)
      if(_intervals.at(i).have_union(_intervals.at(i+1))){
        interval<T> intv = _intervals.at(i).intv_union(_intervals.at(i+1));
        _intervals.at(i) = intv;
        _intervals.erase(_intervals.begin()+i+1);
      }else
        i++;
  }

  /**
   * 
   */
  po_set set_intersect(po_set<T>& s){
    vector<interval<T>> new_intervals;
    for(int i = 0; i < _intervals.size(); i++)
      for(int j = 0; j < s._intervals.size(); j++)
        if(_intervals.at(i).have_intersect(s._intervals.at(j)))
          new_intervals.push_back(_intervals.at(i).intv_intersect(s._intervals.at(j)));
    return po_set(new_intervals);
  }

  po_set set_union(po_set<T>& s){
    vector<interval<T>> new_intervals;
    for(int i = 0; i < _intervals.size(); i++)
      for(int j = 0; j < s._intervals.size(); j++)
        if(_intervals.at(i).have_union(s._intervals.at(j)))
          new_intervals.push_back(_intervals.at(i).intv_union(s._intervals.at(j)));
        else{
            new_intervals.push_back(_intervals.at(i));
            new_intervals.push_back(s._intervals.at(j));
        }
    return po_set(new_intervals);
  }

  po_set difference(po_set<T>& u);

  po_set complement(po_set<T>& u);

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
