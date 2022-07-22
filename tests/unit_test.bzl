load("@pip_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_test")

def glob_to_individual_py_tests(files):
    for name in files:
        py_test(
            name = name.replace(".", "_"),
            srcs = [name],
            deps = [
                ":test",
                "//mrtl:lib",
                requirement("jinja2"),
            ],
            main = name,
        )
