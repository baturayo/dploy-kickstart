#' @dploy endpoint predict
def f1(x):
    return x["val"]


#' @dploy endpoint train
def f2(x):
    return x


# @dploy endpoint performance
# @dploy report_return_value
def my_func4(x):
    return {"_performance": x}
