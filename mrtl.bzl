def mrtl_test(name, srcs, ignored=[], waivers=[], tags=[]):
    """Run meticulous_rtl on source files."""
    ignore_config = ["//digital/rtl/scripts:mrtl.ignore"] + waivers

    args = [
                "--rc $(location @meticulous_rtl//mrtl:lw_rc.py)",
                " ".join(["$(locations {})".format(s) for s in srcs]),
    ]

    data = srcs + ["@meticulous_rtl//mrtl:lw_rc.py", "@meticulous_rtl//mrtl:lib"] + ignore_config

    for igr in ignored:
        args.append("--igr {}".format(igr))
    for igrc in ignore_config:
        args.append("--igrc $(location {})".format(igrc))

    # Need to leave this as a native.py_test instead of @rules_python because some versions of rules_python
    # can't pass tags properly
    native.py_test(
        name = name,
        srcs = ["@lintworks//:main"],
        data = data,
        args = args,
        main = "@lintworks//:main.py", # Seems silly that this is necessary
        tags = tags,
    )
