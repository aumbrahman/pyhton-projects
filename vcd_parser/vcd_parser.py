def parse_header(lines):
    symbol_to_name = {}
    for line in lines:
        line = line.strip()
        if line.startswith('$var'):
            parts = line.split()
            symbol = parts[3]
            name = parts[4]
            symbol_to_name[symbol] = name
        if line.startswith('$enddefinitions'):
            break
    return symbol_to_name


def parse_body(lines, symbol_to_name):
    events = []
    current_time = 0
    started = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('$enddefinitions'):
            started = True
            continue
        if not started:
            continue

        if line.startswith('#'):
            current_time = int(line[1:])
        else:
            value = line[0]
            symbol = line[1:]
            if symbol in symbol_to_name:
                name = symbol_to_name[symbol]
                events.append((current_time, name, value))

    return events


def parse_vcd(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    symbol_to_name = parse_header(lines)
    events = parse_body(lines, symbol_to_name)
    return symbol_to_name, events