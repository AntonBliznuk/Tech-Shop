def page_manager(my_list, page_number : int, items_on_page : int):
    return my_list[(page_number - 1)*items_on_page: items_on_page*page_number]


if __name__ == '__main__':
    print(page_manager([1, 2, 3], 2, 4))
