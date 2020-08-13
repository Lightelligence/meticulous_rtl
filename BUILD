py_library(
    name = "lib",
    srcs = glob(["mrtl/*.py"]),
    deps = ["@lintworks//:lib"],
    visibility = ["//visibility:public"],
)

exports_files([
    "mrtl/lw_rc.py",
])


py_library(
    name = "test",
    srcs = ["test.py"],
)

load("//:unit_test.bzl", "glob_to_individual_py_tests")

glob_to_individual_py_tests(
    files = glob(["tests/*.py"]),
)
