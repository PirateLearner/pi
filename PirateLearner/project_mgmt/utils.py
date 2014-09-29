
import sys
import os
import ConfigParser

def parse_feature():
    """
    open the feature.ini file and pass each section to the funtion pase_section() and reture list of dictionary 
    """
    try:
        Config = ConfigParser.ConfigParser()
        filename = os.path.abspath(os.path.dirname(__file__))+"/"+ "features.ini"
        Config.read(filename)
        return_list = []
        for section in Config.sections():
            return_list.append(parse_section(Config,section))
        return return_list
    except OSError as e:
        raise

def parse_section(Config, section):
    """
    parse the options in the section given and return the dictionary 
    """
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1