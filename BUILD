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

py_binary(
    name = "gen_rule_docs",
    srcs = ["gen_rule_docs.py"],
    deps = [
        ":test",
        ":lib",
    ],
)

genrule(
    name = "rendered_rule_docs_md",
    srcs = [":lib"],
    tools = [":gen_rule_docs"],
    outs = ["rendered_rule_docs.md"],
    cmd = "python $(location :gen_rule_docs) > $@",
)

sh_test(
    name = "golden_doc_test",
    size = "small",
    srcs = ["tests/passthrough.sh"],
    data = [
        "rule_docs.md",
        ":rendered_rule_docs_md",
        ":lib",
    ],
    args = ["diff $(location :rule_docs.md) $(location :rendered_rule_docs_md)"],
    tags = ["gold"],
)
