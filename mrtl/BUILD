load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "lib",
    srcs = glob(["*.py"]),
    visibility = ["//visibility:public"],
    deps = ["@lintworks//:lib"],
)

exports_files([
    "lw_rc.py",
])
