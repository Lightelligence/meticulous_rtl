load("@pip_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "gen_rule_docs",
    srcs = ["gen_rule_docs.py"],
    deps = [
        "//mrtl:lib",
        "//tests:test",
        requirement("jinja2"),
    ],
)

genrule(
    name = "rendered_rule_docs_md",
    srcs = ["//mrtl:lib"],
    outs = ["rendered_rule_docs.md"],
    cmd = "python $(location :gen_rule_docs) > $@",
    tools = [":gen_rule_docs"],
)

sh_test(
    name = "golden_doc_test",
    size = "small",
    srcs = ["passthrough.sh"],
    args = ["diff $(location :rule_docs.md) $(location :rendered_rule_docs_md)"],
    data = [
        "rule_docs.md",
        ":rendered_rule_docs_md",
        "//mrtl:lib",
    ],
    tags = ["gold"],
)
