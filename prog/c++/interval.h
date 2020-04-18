#ifndef _INTERVAL_H_
#define _INTERVAL_H_

#include <vector>

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
  interval(const T& l, const T& u, bool li, bool ui) : lower_inc(li), upper_inc(ui){
    lower = l;
    upper = u;
    if (u < l || (lower == upper && !(lower_inc && upper_inc))){
      lower = T(0); upper = T(0); lower_inc = 0; upper_inc = 0;
    }
  }

  /**
   * Checks if a value is bounded by the interval
   *
   * @param element the value to be checked
   * @return
   */
  bool contains(const T& element) const{
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
    return (lower_inc ? "[" : "(" ) + lower.to_string() + ","
                                    + upper.to_string() + (upper_inc ? "]" : ")");
  }
};

#endif
