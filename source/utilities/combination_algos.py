def get_combination(numbers, markers):
    result = {'extracted': [], 'remaining': []}
    for (item, status) in zip(numbers, markers):
        if status:
            result['extracted'].append(item)
        else:
            result['remaining'].append(item)
    return result


def generate_combination_implement(numbers, markers, n, k, pos, result):
    if k == 0:
        return
    for i in range(pos, n):
        if not markers[i]:
            markers[i] = True
            if k - 1 == 0:
                result.append(get_combination(numbers, markers))
            else:
                generate_combination_implement(numbers, markers, n, k - 1, i + 1, result)
            markers[i] = False


def generate_combination(numbers, n, k):
    markers = [False for _ in range(n)]
    result = []
    generate_combination_implement(numbers, markers, n, k, 0, result)
    return result  # result: [{extracted: [], remaining: []}]
