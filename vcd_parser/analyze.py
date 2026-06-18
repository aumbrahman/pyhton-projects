from collections import Counter, defaultdict

from vcd_parser import parse_vcd

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def toggle_counts(events):
    counts = Counter()
    for _, name, _ in events:
        counts[name] += 1
    return counts


def build_signal_timeline(events, max_signals=5):
    signal_order = []
    signal_events = defaultdict(list)

    for t, name, val in events:
        if name not in signal_order:
            signal_order.append(name)
        if len(signal_order) <= max_signals or name in signal_order[:max_signals]:
            signal_events[name].append((t, val))

    selected = signal_order[:max_signals]
    return selected, signal_events


def value_to_level(value):
    mapping = {
        "0": 0,
        "1": 1,
        "x": 0.5,
        "z": 0.25,
        "b": 0.75,
    }
    return mapping.get(value, 0.5)


def plot_waveforms(events, max_signals=5):
    if plt is None:
        print("matplotlib is not installed")
        return

    selected, signal_events = build_signal_timeline(events, max_signals=max_signals)
    if not selected:
        print("No waveform data to plot.")
        return

    plt.figure(figsize=(12, 2 + len(selected)))
    for idx, name in enumerate(selected):
        data = signal_events[name]
        if not data:
            continue

        times = [t for t, _ in data]
        levels = [value_to_level(v) + idx * 2 for _, v in data]
        plt.step(times, levels, where='post', label=name)
        plt.scatter(times, levels, s=20)

    plt.yticks([idx * 2 for idx in range(len(selected))], selected)
    plt.xlabel('Time')
    plt.title(f'Waveform for first {len(selected)} signals')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()


def plot_toggle_counts(counts, top_n=10):
    if plt is None:
        print("matplotlib is not installed. Install it with 'pip install matplotlib' to see toggle count plots.")
        return

    most_common = counts.most_common(top_n)
    if not most_common:
        print("No toggle counts to plot.")
        return

    names, values = zip(*most_common)
    plt.figure(figsize=(10, 6))
    plt.barh(names[::-1], values[::-1], color='tab:blue')
    plt.xlabel('Toggle Count')
    plt.title(f'Top {len(names)} Signal Toggle Counts')
    plt.tight_layout()


if __name__ == "__main__":
    symbols, events = parse_vcd("wave.vcd")

    print("Signals found:", list(symbols.values()))
    print("\nFirst 10 events:")
    for t, name, val in events[:10]:
        print(t, name, val)

    print("\nToggle counts:")
    counts = toggle_counts(events)
    for name, count in counts.items():
        print(name, "->", count, "toggles")
    if plt is not None:
        plot_waveforms(events, max_signals=5)
        plot_toggle_counts(counts, top_n=10)
        plt.show()
    else:
        print("\nInstall matplotlib with: pip install matplotlib")