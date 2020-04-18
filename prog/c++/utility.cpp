#include <vector>
#include "utility.h"

int main(int argc, char const *argv[]) {
  pugi::xml_document doc;
  pugi::xml_parse_result result = default_load_document("chem", doc);
  pugi::xml_node root = doc.document_element();
  auto elem = root.child("course").find_child_by_attribute("course_info", "name", "grading");
  std::cout << elem.child_value() << '\n';
}

vector<course_tree> generate_course_tree_from_xml(const pugi::xml_document& doc){
  pugi::xml_node root = doc.document_element();
  vector<course_tree> v;
  for (pugi::xml_node courses = root.child("course"); courses; courses = c.next_sibling("course")){
    std::string name = courses.attribute("name").value();
    double units = std::stod(courses.find_child_by_attribute("course_info", "name", "units").child_value());
    grading option = stog(courses.find_child_by_attribute("course_info", "name", "grading").child_value());
    course_tree t(name, units, option);
    for (pugi::xml_node lectures = root.child("lecture"); lectures; lectures = c.next_sibling("lecture")){
      int id = std::stoi(lectures.find_child_by_attribute("lecture_info", "name", "id").child_value());
      std::string days = std::stoi(lectures.find_child_by_attribute("lecture_info", "name", "id").child_value());
      int id = std::stoi(lectures.find_child_by_attribute("lecture_info", "name", "id").child_value());
      int id = std::stoi(lectures.find_child_by_attribute("lecture_info", "name", "id").child_value());
      int id = std::stoi(lectures.find_child_by_attribute("lecture_info", "name", "id").child_value());
    }
  }
}

grading stog(const std::string& option) const{
  if(option == "Grading:Optional")
    return grading::Optional;
  if(option == "Letter Graded")
    return grading::Letter;
  if(option == "Pass/No Pass")
    return grading::Letter;
}

class_time stot(const char& day, const interval<integer>& time) const{
  switch (day) {
    case 'M':

    case 'T':
    case 'W':
    case 'R':
    case 'F':
    case 'S':
    case 'U':
  }
}

pugi::xml_parse_result load_document_from_path(const std::string& path, pugi::xml_document& doc){
  return doc.load_file(path.c_str());
}

pugi::xml_parse_result default_load_document(const std::string& filename, pugi::xml_document& doc){
  std::string path = OUTPUT_DEFAULT_FOLDER + filename;
  if(!filename.length() > 4 || !(filename.substr(filename.length() - 4, filename.length()) == ".xml"))
    path += ".xml";
  return load_document_from_path(path, doc);
}
