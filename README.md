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
The following contains a compilation of the mrtl rules and the reasons for checking them:

## Always
```
SystemVerilog adds three new types of procedural always blocks that more clearly express intent. 
These are: always_comb, always_latch, and always_ff. Simulation, lint, and synthesis can issue warnings 
if the code modeled within these new procedural blocks does not match the designated type. This is a safer
and more explicit coding style as opposed to a simple always block like one would see in traditional Verilog.

We only allow always_comb and always_ff here, because use of latches is generally not preffered, unless in unique circumstances. If such a circumstance arises, use always_latch, and waive this check.
```

## CaseXZ
``` 
SystemVerilog introduced the case...inside statement to replace casex and casez.
casex treats X's as don't cares if they are in the case expression or the case item. 
Pre-synthesis simulations will not propagate X's, but the X's will propagate in gate-sim (if one is run at all).
casez is has similar behavior as casex, but the X's are Z's. This type of simulation/synthesis mis-match is
dangerous, and is what case...inside is intended to fix. Always use case...inside instead of casex or casez.
Also beware that using case...inside with a default case can still lead to X-prop issues. the safest coding
scheme, when it comes to case statements in general, is to write an assertion that checks whether the case expression 
has an X in it. A more detailed analysis of this can be found here: https://lcdm-eng.com/papers/snug12_Paper_final.pdf
```

## Clk
```
Changing clock names through hierarchy is dangerous because it is difficult
to catch RTL clock wiring bugs in simulation. It is acceptable to change names if you
are going from more-specific to less specific like in the following examples:
.clk (eclk)
or
.sclk(ccu31_sclk)
however, it is illegal to completely change clock names on the boundary like:
.eclk(sclk)
```

## ImportWildcard
```
This is anything of the format 'import <pkg>::*'.

While doing an import by wildcard may reduce the amount of typing you need
to do in your module and you could argue it improves readability, it makes
tracing much more difficult.

Params and types no longer indicate their parent package which is where you would find their definition.

By explicitly refering to content withing a package, you know implcilitly
where the definition lives. It also makes it more obvious how tightly
coupled a module is to a package: you can easily count the number of
references to the package.
```

## MagicNumbers
```
In our systemverilog methodology, try to put as many types and parameters either into systemverilog typedefs (or typedef unions or typdef structs) or into localparams. Use typdefs as much as possible since the type name conveys intent (e.g. edl_cmd_t), but in some cases localparams or parameters (e.g. logic [chip_rypkg::NUM_DPM_ENG - 1:0])to define a logic width is okay.
A declaration like "logic [5:0]" is bad because it doesn't relate to any other defined type. 
Also, "logic [chip_rypkg::NUM_DPM_ENG - 3:0]" is bad because we don't know where the 3 comes from. 
It's safe enough to waive "-1" because it's a common pattern, but everything else it should be banned.
i.e. [VAR_NAME -1:0]
For loop formatting should follow:

for (var_name= 0; var_name < parameter_or_localparam; var_name++) begin : label_name
```

## ModuleDeclaration
```
Format module declaration using 'module <module_name>' on its own line, then a newline with 2 spaces and open paren, then newline and signals)

e.g.
module eu
  (
```

## ModuleName
```
Module names shoulds match the file name to improve navigation.
If a module name matches its filename, its definition can be found intuitively  
```

## MultiDimArray
```
Multi-dimmensional arrays are considered complex data types. They should be defined as typedefs in
YIS for the purpose of type-safety and documentation.
```

## MultipleModules
```
Each module should be in its own file.

There are two main reasons to keep each module in its own file:
  1. Readability
    Files remain a reasonable size.
  2. Navigation
    If a module name matches its filename, its defintion can be found intuitively.
```

## Types
```
Synthesizable SV RTL should only use a subset of all SV types available.
Ban the following types: bit, real, integer (should use int instead), string, byte, shortint, longint, wand, wor, tri, triand, trior, tri0, tri1, supply0, supply1, trireg, shortreal, realtime, class
```

## UnpackedVector
```
Unpacked vectors are less efficient in memory, waveform programs sometimes don't render them correctly, and you can't assign to the entire vector at once (such as in reset blocks). Avoid usage.
```
