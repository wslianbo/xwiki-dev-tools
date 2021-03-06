import fnmatch
import os
import re
import sys

from common import XmlFile, PropertiesFile

def properties_to_xwiki_xml(path, path_prefix, lang):
    """Convert a java properties file to an XWiki XML file"""
    relative_dir_path = os.path.dirname(path)
    file_name = os.path.basename(path).split(".")[0]

    properties_path = "{}.translation/{}_{}.properties".format(
        path_prefix, relative_dir_path + "/" + file_name, lang)
    properties = PropertiesFile()
    with open(properties_path, "r") as f_properties:
        properties.load(f_properties.read())

    title = properties.get_value("{}.title".format(file_name))
    content = properties.get_value("{}.content".format(file_name))
    xml_file = XmlFile(path_prefix + path)
    xml_file.set_tag_content("title", title)
    xml_file.set_tag_content("content", content)
    xml_file.write()

def properties_to_xwiki_xml_properties(path, path_prefix, lang):
    """Convert a java properties file to an XWiki XML file with properties"""
    relative_dir_path = os.path.dirname(path)
    file_name = os.path.basename(path).split(".")[0]

    properties_path = "{}.translation/{}_{}.properties".format(
            path_prefix, relative_dir_path + "/" + file_name, lang)
    properties = PropertiesFile()
    with open(properties_path, "r") as f_properties:
        properties.load(f_properties.read())

    xml_file = XmlFile(path_prefix + path)
    xml_file.set_tag_content("content", properties.document)
    xml_file.write()

def properties_to_xwiki_properties(path, path_prefix, lang):
    """Convert a java properties file to an XWiki java properties file"""
    relative_dir_path = os.path.dirname(path)
    file_name = os.path.basename(path).split(".")[0]
    lang_delimiter_index = file_name.rfind("_")
    if lang_delimiter_index > 0:
        file_name = file_name[:lang_delimiter_index]

    properties_path = "{}.translation/{}_{}.properties".format(
            path_prefix, relative_dir_path + "/" + file_name, lang)
    with open(properties_path, "r") as f_properties:
        with open(path_prefix + path, "w") as f_wiki_properties:
            f_wiki_properties.write(f_properties.read())

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    PATH_PREFIX = os.environ["WL_PATH"] if "WL_PATH" in os.environ else ""
    if PATH_PREFIX and PATH_PREFIX[-1] != "/":
        PATH_PREFIX += "/"
    TRANSLATION_WIKI_FILE_NAME = sys.argv[1] if len(sys.argv) > 1 else "translation_wiki.txt"
    if len(sys.argv) > 2:
        TRANSLATION_WIKI_PROPERTIES_FILE_NAME = sys.argv[2]
    else:
        TRANSLATION_WIKI_PROPERTIES_FILE_NAME = "translation_wiki_properties.txt"
    if len(sys.argv) > 3:
        TRANSLATION_PROPERTIES_FILE_NAME = sys.argv[3]
    else:
        TRANSLATION_PROPERTIES_FILE_NAME = "translation_properties.txt"

    with open(TRANSLATION_WIKI_FILE_NAME, 'r') as f:
        for line in f.read().splitlines():
            properties_to_xwiki_xml(line, PATH_PREFIX, "en")
            dir_name = os.path.dirname(line)
            name = os.path.basename(line).split(".")[0]
            for file_name in os.listdir(PATH_PREFIX + dir_name):
                if fnmatch.fnmatch(file_name, "{}.*.xml".format(name)):
                    lang = file_name.split(".")[-2]
                    if lang != "en":
                        properties_to_xwiki_xml(dir_name + "/" + file_name, PATH_PREFIX, lang)
    with open(TRANSLATION_WIKI_PROPERTIES_FILE_NAME, 'r') as f:
        for line in f.read().splitlines():
            properties_to_xwiki_xml_properties(line, PATH_PREFIX, "en")
            dir_name = os.path.dirname(line)
            name = os.path.basename(line).split(".")[0]
            for file_name in os.listdir(PATH_PREFIX + dir_name):
                if fnmatch.fnmatch(file_name, "{}.*.xml".format(name)):
                    lang = file_name.split(".")[-2]
                    if lang != "en":
                        properties_to_xwiki_xml_properties(
                            dir_name + "/" + file_name, PATH_PREFIX, lang)
    with open(TRANSLATION_PROPERTIES_FILE_NAME, 'r') as f:
        for line in f.read().splitlines():
            properties_to_xwiki_properties(line, PATH_PREFIX, "en")
            dir_name = os.path.dirname(line)
            name = os.path.basename(line).split(".")[0]
            for file_name in os.listdir(PATH_PREFIX + dir_name):
                if fnmatch.fnmatch(file_name, "{}_*.properties".format(name)):
                    lang = file_name.split(".")[0]
                    lang = lang[lang.rfind("_") + 1:]
                    if lang != "en":
                        properties_to_xwiki_properties(
                            dir_name + "/" + file_name, PATH_PREFIX, lang)
