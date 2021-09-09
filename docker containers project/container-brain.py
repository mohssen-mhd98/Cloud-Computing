import sys
import os
from io import StringIO
import contextlib


# input.txt => list
def scan_file(path):
    with open(path, 'r') as file:
        contents = file.read().split()
        return contents


def get_min(token_list):
    float_list = [float(x) for x in token_list]
    return min(float_list)


def get_max(token_list):
    float_list = [float(x) for x in token_list]
    return max(float_list)


def get_average(token_list):
    sum = 0
    for token in token_list:
        sum += float(token)
    return sum / len(token_list)


def sort_list(token_list):
    float_list = [float(x) for x in token_list]
    return sorted(float_list)


def word_count(token_list):
    words = {}
    final_list = []
    for token in token_list:
        if token not in words.keys():
            words[token] = 1
        else:
            words[token] += 1
    sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
    for word in sorted_words:
        final_list.append([word[0], word[1]])

    return final_list


def write_output(input_list, operand, arg):
    i = 0
    while os.path.exists(f"{arg}/{operand}_{i}.txt"):
        i += 1
    filename = f"{operand}_{i}.txt"

    with open(f"{arg}/{filename}", "w") as f:
        if type(input_list) is list:
            for item in input_list:
                if isinstance(item, list):
                    f.write("%s     %s\n" % (item[0], item[1],))
                else:
                    f.write("%s\n" % item)
        else:
            f.write(str(input_list))
        f.close()


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


if __name__ == '__main__':
    args = sys.argv
    a = scan_file(args[2])

    if args[1] == "min":
        write_output(get_min(a), "min", args[3])
        print("done")
    elif args[1] == "max":
        write_output(get_max(a), "max", args[3])
        print("done")
    elif args[1] == "average":
        write_output(get_average(a), "average", args[3])
        print("done")
    elif args[1] == "sort":
        write_output(sort_list(a), "sort", args[3])
        print("done")
    elif args[1] == "Wordcount":
        write_output(word_count(a), "Wordcount", args[3])
        print("done")
    elif args[1][-3:] == ".py":
        with stdoutIO() as s:
            exec(open(args[2]).read())
        write_output(s.getvalue(), args[1][:-3], args[3])
    else:
        print("Wrong input. Please try again!")
