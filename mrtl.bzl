def mrtl_test(name, srcs, tags=[]):
    """Run meticulous_rtl on source files."""
    data = srcs + ["@meticulous_rtl//mrtl:lw_rc.py", "@meticulous_rtl//mrtl:lib"]

    # Need to leave this as a native.py_test instead of @rules_python because some versions of rules_python
    # can't pass tags properly
    native.py_test(
        name = name,
        srcs = ["@lintworks//:main"],
        data = data,
        args = [
            "--rc $(location @meticulous_rtl//mrtl:lw_rc.py)",
            " ".join(["$(locations {})".format(s) for s in srcs]),
        ],
        main = "@lintworks//:main.py", # Seems silly that this is necessary
        tags = tags,
    )
