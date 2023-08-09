import requests

def convert_response(response):
    filter_list = list(response.split("\n"))
    final_list = [x for x in filter_list if(not x.startswith("!"))]
    return final_list


#return type of the filter per filter line
def classify_filter(filter_type):
    if '#$#' in filter_type:
        return 'snippet'
    elif '#@#' in filter_type:
        return 'elem_hide_pseudo'
    elif '#?#' in filter_type:
        return 'elem_hide_pseudo'
    # elif '##' in filter_type:
    #     return 'elem_hide'
    # elif "#@#" in filter_type:
    #     return 'allowlist_elem_hide'
    # elif filter_type.startswith('|'):
    #     return 'network_request_block'
    # elif filter_type.startswith('@@|'):
    #     return 'allowlist_network_request'
    else:
        return 'blocking_filters'

#declare dictionary of filter types
filter_categories = {
    # snippets only
    "snippet": [],
    # only filters with #?#, #@#
    "elem_hide_pseudo": [],
    # "elem_hide":  [],
    # "allowlist_elem_hide": [],
    # "network_request_block": [],
    # "allowlist_network_request": [],
    "blocking_filters": []
    }


#main logic
if __name__ == '__main__':
    url = input("Please add the url of the file you would like to separate: ")
    name_prefix = input("Enter a prefix for new lists: ")
    list_request = requests.get(url).text
    list_to_filter = convert_response(list_request)
    for list_line in list_to_filter:
        filter_type = classify_filter(list_line)
        filter_categories[filter_type].append(list_line)
    for category in filter_categories:
        # create the list only if it's not empty
        if len(filter_categories[category]) > 0:
            f = open(f'{name_prefix}_{category}.txt','w')
            f.write(list_to_filter[0] + "\n")
            lines_to_print = filter_categories[category]
            f.writelines([x + "\n" for x in lines_to_print])
            f.close()




