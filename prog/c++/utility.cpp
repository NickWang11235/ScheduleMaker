#include <vector>
#include "utility.h"

int main(int argc, char const *argv[]) {
  pugi::xml_document doc;
  pugi::xml_parse_result result = default_load_document("chem", doc);
  pugi::xml_node root = doc.document_element();
  std::cout << root.child("course").name() << '\n';
}

tree generate_course_tree_from_xml(pugi::xml_document doc){
  pugi::xml_node root = doc.document_element();
  vector<course> v;
  for (pugi::xml_node courses = tools.child("course"); courses; courses = c.next_sibling("course")){
    int id =
    course c =
    v.push_back()
  }
}

pugi::xml_parse_result load_document_from_path(const std::string path, pugi::xml_document& doc){
  return doc.load_file(path.c_str());
}

pugi::xml_parse_result default_load_document(const std::string filename, pugi::xml_document& doc){
  std::string path = OUTPUT_DEFAULT_FOLDER + filename;
  if(!filename.length() > 4 || !(filename.substr(filename.length() - 4, filename.length()) == ".xml"))
    path += ".xml";
  return load_document_from_path(path, doc);
}
