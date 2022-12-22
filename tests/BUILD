load("@rules_python//python:defs.bzl", "py_library")
load("@meticulous_rtl//tests:unit_test.bzl", "glob_to_individual_py_tests")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "test",
    srcs = ["test.py"],
)

glob_to_individual_py_tests(
    files = glob(["*.py"]),
)
