#ifndef _UTILITY_H_
#define _UTILITY_H_

#include <string>
#include <iostream>

#include "pugixml.hpp"
#include "schedule_search.h"
#include "constants.h"

course generate_course_tree_from_xml();
pugi::xml_parse_result load_document_from_path(const std::string path, pugi::xml_document& doc);
pugi::xml_parse_result default_load_document(const std::string filename, pugi::xml_document& doc);

#endif
