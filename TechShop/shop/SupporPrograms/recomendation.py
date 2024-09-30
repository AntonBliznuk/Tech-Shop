import random


def no_data_rec(product_list, how_many):
    result = []
    while len(result) <= how_many:
        item = random.choice(product_list)
        if item not in result:
            result.append(item)

    return result


if __name__ == '__main__':
    print(no_data_rec([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 13))
