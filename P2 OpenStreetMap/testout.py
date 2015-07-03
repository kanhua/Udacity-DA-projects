import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict


def sort_dictionary_by_count(dictionary, top = None):
    if top is None:
        top = len(dictionary)

    keys_dict = list(dictionary.keys())
    keys_dict.sort(key = lambda k : dictionary[k], reverse=True)
    count = 0

    for key in keys_dict:
        if top == count:
            break
        print("{} => {}".format(key, dictionary[key]))
        count += 1


def unique_tags(filename):
    tag_dict = defaultdict(int)
    for events, element in ET.iterparse(filename, events = ('start','end')):
        if events == 'end':
            tag_dict[element.tag] += 1

    return tag_dict


def tags_k_value(filename):
    tag_dict = defaultdict(int)
    for events, element in ET.iterparse(filename, events = ('start','end')):
        if events == 'end' and element.tag == 'tag':
            tag_dict[element.attrib['k']] += 1

    return tag_dict


def religion(filename):
    religion_names = defaultdict(int)
    for events, element in ET.iterparse(filename):
        if events == 'end' and element.tag == 'tag':
            if element.attrib['k'] == 'religion':
                #print("add another %s"%element.attrib['v'])
                religion_names[element.attrib['v']] += 1
            element.clear()
    return religion_names


if __name__ == '__main__':

    import time
    starttime=time.time()
    d = religion('./osm data/san-francisco-bay_california.osm')
    # d = tags_k_value('bangalore_test_map.osm')
    # pprint.pprint(d)
    sort_dictionary_by_count(d)
    endtime=time.time()

    print(endtime-starttime)