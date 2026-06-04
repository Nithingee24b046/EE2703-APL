"""Tiny combinational logic simulator producing WaveDrom JSON.

Usage:
  python digitalsim.py path/to/circuit.net [--out out.json]

Input format sections (fixed order): INPUTS, OUTPUTS, GATES, STIMULUS.
Gates: OUT = AND(A, B) | OR(A, B) | XOR(A, B) | NOT(A)

Note: this template file uses the `argparse` module to get arguments
from the command line.  You are expected to retain this part of it
to make testing easier.  The function calls given in the `main` function
are only suggestions, and you can rename them or create others as long
as the interface to the outside world does not change.

This may make it a bit harder to run purely from an editor like VSCode. 
However, in practice you almost never run code directly from an editor,
so this is something you need to be able to handle anyway.
"""

"""
Name : Nithin G
Roll number : EE24B046
Materials Used : GPT to learn about json format files and to implement to_wavedrom function which I don't know
"""

import sys
import argparse
from pathlib import Path
from typing import List

gate_set = ["AND", "NOT", "OR", "XOR"]

def parse_netlist(text: str):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]

    #define a function to locate the lines with a particular prefix
    def expect(prefix: str, idx: int) -> int:
        if idx >= len(lines) or not lines[idx].startswith(prefix):
            raise ValueError(f"Expected '{prefix}' section")
        return idx

    #locate line starting with inputs
    i = expect("INPUTS:", 0)
    try:
        rest = lines[i].split(":", 1)[1].strip()
        if not rest:
            raise ValueError("No inputs specified after 'INPUTS:'")
        inputs = rest.split()
    except (IndexError, ValueError):
        raise ValueError("Invalid 'INPUTS:' line format")
    i += 1

    #locate line starting with inputs
    i = expect("OUTPUTS:", i)
    try:
        rest = lines[i].split(":", 1)[1].strip()
        if not rest:
            raise ValueError("No inputs specified after 'OUTPUTS:'")
        outputs = rest.split()
    except (IndexError, ValueError):
        raise ValueError("Invalid 'OUTPUTS:' line format")
    i += 1

    #locate the index of element like "STIMULUS"
    gate_index = lines.index("STIMULUS:")
    #creating the tuple of gates
    gates = []
    try:
        if lines[i+1] == "STIMULUS:":
            raise ValueError("No inputs specified after 'GATES:'")
    except (IndexError, ValueError):
        raise ValueError("Invalid 'GATES:' line format")
    
    for x in range(i+1,gate_index):
        out = lines[x].split("=", 1)[0].strip() #output variable
        typ = lines[x].split("=", 1)[1].strip().split("(", 1)[0].strip() #gate type
        args = [a.strip() for a in lines[x].split("=", 1)[1].strip().split("(", 1)[1].split(")")[0].split(",")] #args as the input to gate
        gates.append((out, typ, args))

    #reject unknown gates or mismatched input counts.
    for x in gates:
        if x[1] not in gate_set:
            raise ValueError(f"Invalid gate '{x[1]}'. Expected one of {gate_set}")
        elif x[1] != "NOT" and len(x[2]) != 2:
            raise ValueError(f"Gate {x[1]} expects 2 inputs but got {len(x[2])}")
        elif x[1] == "NOT" and len(x[2]) != 1:
            raise ValueError(f"Gate {x[1]} expects 1 input but got {len(x[2])}")

    
    #creating the set of stimulus
    stimulus = []
    times = []
    if gate_index == len(lines) - 1:
        raise ValueError("No lines found after 'STIMULUS:'")

    for x in range(gate_index+1, len(lines)):
        stimulus_elements = lines[x].split(" ", 1)[1].strip()
        time_stamp = lines[x].split(" ", 1)[0].strip()
        stimulus_elements = [int(a.strip()) for a in stimulus_elements.split(" ")]
        times.append(time_stamp)
        stimulus.append(stimulus_elements)
    
    #reject unsorted time stamps/ duplicate time stamps
    if len(times) != len(set(times)):
        raise ValueError("Duplicate timestamps in STIMULUS section")

    if times != sorted(times, key=lambda x: int(x)):
        raise ValueError("Timestamps are not sorted")

    #final dictionary
    broken_netlist = {"inputs": inputs, "outputs" : outputs, "gates" : gates, "stimulus": stimulus}
        
    return broken_netlist

def eval_gate(): #not needed
    pass

def simulate(nl):
    inputs = nl["inputs"]
    outputs = nl["outputs"]
    gates = nl["gates"]
    stim = nl["stimulus"]

    results = []

    for row in stim:
        values = dict(zip(inputs, row))  #start with input assignments

        #keep evaluating gates until all outputs computed
        remaining = gates[:]
        while remaining:
            next_round = []
            for out, gtype, ins in remaining:
                #check if inputs to this gate are all ready
                if all(x in values for x in ins):
                    a = values[ins[0]]
                    b = values[ins[1]] if len(ins) > 1 else None

                    if gtype == "AND":
                        values[out] = a & b
                    elif gtype == "OR":
                        values[out] = a | b
                    elif gtype == "XOR":
                        values[out] = a ^ b
                    elif gtype == "NOT":
                        values[out] = 1 - a
                    else:
                        raise ValueError(f"Unknown gate {gtype}")
                else:
                    next_round.append((out, gtype, ins)) #takes care of the topological ordering
            if len(next_round) == len(remaining):
                raise RuntimeError("Cannot resolve gate dependencies")
            remaining = next_round

        results.append({sig: values[sig] for sig in inputs + outputs})

    return results

def to_wavedrom_json(nl, waves):
    inputs = nl["inputs"]
    outputs = nl["outputs"]
    all_signals = inputs + outputs

    js = '{\n  "signal": [\n'
    for idx, name in enumerate(all_signals):
        pattern = "".join(str(w[name]) for w in waves)
        js += f'    {{"name": "{name}", "wave": "{pattern}"}}'
        if idx != len(all_signals) - 1:
            js += ","
        js += "\n"
    js += "  ]\n}"
    return js


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("netlist", help=".net file path")
    ap.add_argument("--out", "-o", help="output JSON path")
    args = ap.parse_args(argv)

    # Read from the command line argument
    text = Path(args.netlist).read_text()
    nl = parse_netlist(text)
    waves = simulate(nl)
    js = to_wavedrom_json(nl, waves)

    # Automatically generate output path from input filename
    # if not explicitly provided
    out_path = args.out
    if not out_path:
        p = Path(args.netlist)
        out_path = str(p.with_suffix(".json"))
    Path(out_path).write_text(js + "\n")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
