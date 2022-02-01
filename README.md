What is meticulous_rtl?
======================

meticulous_rtl (or mrtl) is a barebones checker for some best-practices in SystemVerilog RTL design.
mrtl doesn't implement a full parser and compiler - all checking is based on Python regular expressions.

When you run a mrtl test (using the mrtl_test bazel rule), mrtl analyzes the target RTL and flags each failing rule and line individually.
Take the following failure for example:
```
digital/rtl/eu/eu_core_cmd_tx.sv:53 violates MultiDimArray
  Reason:
    Multidimensional array of logic type detected. Use YIS to create a typedef instead.
  Offending Code:
    >  logic [chip_rypkg::NUM_UMEM_RD_LANE-1:0][iid_rypkg::NUM_INFLIGHT_INSTR-1:0] umem_rd_cmd_vld;
```
Each failure will give a failing rule name (in this case MultiDimArray) and the reason for why the RTL failed the rule.
Additionally, mrtl gives the failing file and line number and also the raw failing text.

Failing RTL should be fixed to adhere to best practices.
However, in the rare cases that the RTL won't be fixed and a rule needs to be fixed, mrtl has a built-in waiver syntax.
Each waiver needs a disable and an enable line to turn off and on individual rules. The following example turns off the
MultiDimArray rule for two lines of RTL:

```
  // waiving because this is just TB code
  // mrtl: disable=MultiDimArray
  logic [chip_rypkg::NUM_UMEM_RD_LANE-1:0][iid_rypkg::NUM_INFLIGHT_INSTR-1:0] umem_rd_cmd_vld;
  logic [chip_rypkg::NUM_UMEM_WR_LANE-1:0][iid_rypkg::NUM_INFLIGHT_INSTR-1:0] umem_wr_cmd_vld;
  // mrtl: enable=MultiDimArray
```

In general, the syntax is:

`// mrtl: (disable|enable)=[Comma separated list of rules]`

# List of Rules
The full list of rules and documentation [are listed here](https://dev.azure.com/LightelligencePlatform/meticulous_rtl/_git/meticulous_rtl?path=/rule_docs.md&version=GBcg/docs&_a=preview)
