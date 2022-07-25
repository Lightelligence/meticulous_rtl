load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "lib",
    srcs = glob(["*.py"]),
    deps = ["@lintworks//:lib"],
    visibility = ["//visibility:public"],
)

exports_files([
    "lw_rc.py",
])
