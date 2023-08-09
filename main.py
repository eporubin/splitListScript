import requests


def convert_response(response):
    filter_list = list(response.split("\n"))
    final_list = [x for x in filter_list if (not x.startswith("!"))]
    return final_list


def classify_filter(filter_type):
    if '#$#' in filter_type:
        return 'snippet'
    elif ('#@#' in filter_type) or ('#?#' in filter_type):
        return 'elem_hide_pseudo'
    else:
        return 'blocking_filters'


def process_url_list(url_list, name_prefix):
    filter_categories = {
        "snippet": [],
        "elem_hide_pseudo": [],
        "blocking_filters": []
    }

    for url in url_list:
        list_request = requests.get(url).text
        list_to_filter = convert_response(list_request)

        for list_line in list_to_filter:
            filter_type = classify_filter(list_line)
            filter_categories[filter_type].append(list_line)

    for category in filter_categories:
        if len(filter_categories[category]) > 0:
            with open(f'{name_prefix}_{category}.txt', 'w') as f:
                if category != 'blocking_filters':
                    f.write(filter_categories[category][0] + "\n")
                lines_to_print = filter_categories[category]
                f.writelines([x + "\n" for x in lines_to_print])


if __name__ == '__main__':
    url_list = input("Please enter a comma-separated list of URLs: ").split(',')
    name_prefix = input("Enter a prefix for new lists: ")

    process_url_list(url_list, name_prefix)
