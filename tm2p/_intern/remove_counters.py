def remove_counters(x):
    if x == "":
        return x
    return " ".join(x.split(" ")[:-1])
