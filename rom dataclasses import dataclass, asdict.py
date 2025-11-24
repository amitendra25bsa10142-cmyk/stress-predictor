rom dataclasses import dataclass, asdict
from typing import List, Tuple
import csv
import sys


# -------------------------
# Data container
# -------------------------
@dataclass
class Person:
    name: str
    heart_rate_bpm: float
    sleep_hours_per_day: float
    work_hours_per_week: float


# -------------------------
# Predictor class
# -------------------------
class StressPredictor:
    # Human-friendly defaults — tweak these and re-run to see how scores change.
    WEIGHT_HEART_RATE = 0.8   # heart rate influence (normalized by 80 BPM)
    WEIGHT_SLEEP = -1.5       # each hour of sleep reduces the score
    WEIGHT_WORK = 1.0         # work hours influence (normalized by 50 hrs/wk)
    BIAS = 20.0               # baseline starting point for score

    def __init__(self, people: List[Person]):
        """Initialize with a list of Person. None => empty list."""
        self.people = list(people or [])

    # ---- internal helpers ----
    @staticmethod
    def _normalize(person: Person) -> Tuple[float, float, float]:
        """
        Convert raw features into the scales used by the formula.
        Baselines: 80 BPM for heart rate, 50 hours/week for work.
        Sleep is already in hours/day and left as-is (intuitive).
        """
        hr_norm = person.heart_rate_bpm / 80.0
        sleep = person.sleep_hours_per_day
        work_norm = person.work_hours_per_week / 50.0
        return hr_norm, sleep, work_norm

    def predict_score(self, person: Person) -> float:
        """Return a clamped score between 0 and 100. Rounded later by callers if needed."""
        hr, sleep, work = self._normalize(person)
        raw = (
            self.WEIGHT_HEART_RATE * hr
            + self.WEIGHT_SLEEP * sleep
            + self.WEIGHT_WORK * work
            + self.BIAS
        )
        # clamp into [0, 100] so outputs stay sane
        return max(0.0, min(100.0, raw))

    @staticmethod
    def classify(score: float) -> str:
        """Human categories for the numeric score."""
        if score > 70:
            return "High"
        if score > 40:
            return "Moderate"
        return "Low"

    # ---- useful interfaces ----
    def results(self) -> List[Tuple[Person, float, str]]:
        """Return a list of (Person, rounded_score, risk_label)."""
        out = []
        for p in self.people:
            s = round(self.predict_score(p), 1)
            out.append((p, s, self.classify(s)))
        return out

    def pretty_print(self) -> None:
        """Print a friendly, human-readable table to stdout."""
        if not self.people:
            print("No people supplied. Nothing to predict.")
            return

        header = "Name       | HR  | Sleep | Work | Score | Risk"
        print("\n" + header)
        print("-" * len(header))
        for person, score, risk in self.results():
            # Align fields to make the table compact and readable
            print(
                f"{person.name:<10} | "
                f"{person.heart_rate_bpm:>4.0f} | "
                f"{person.sleep_hours_per_day:>5.1f} | "
                f"{person.work_hours_per_week:>4.0f} | "
                f"{score:>5.1f} | {risk}"
            )
        print("-" * len(header))
        print(f"Processed {len(self.people)} record(s). Note: this is a simple estimator, not medical advice.\n")

    # ---- utilities ----
    def save_to_csv(self, filepath: str) -> None:
        """Save results to CSV: name,hr,sleep,work,score,risk"""
        rows = self.results()
        with open(filepath, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["name", "heart_rate_bpm", "sleep_hours_per_day", "work_hours_per_week", "score", "risk"])
            for p, s, r in rows:
                writer.writerow([p.name, p.heart_rate_bpm, p.sleep_hours_per_day, p.work_hours_per_week, s, r])

    @staticmethod
    def load_people_from_csv(filepath: str) -> List[Person]:
        """Load people from CSV with header name,heart_rate_bpm,sleep_hours_per_day,work_hours_per_week"""
        loaded = []
        with open(filepath, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                try:
                    loaded.append(Person(
                        name=row.get("name", "").strip() or "Unnamed",
                        heart_rate_bpm=float(row.get("heart_rate_bpm") or 0),
                        sleep_hours_per_day=float(row.get("sleep_hours_per_day") or 0),
                        work_hours_per_week=float(row.get("work_hours_per_week") or 0),
                    ))
                except ValueError:
                    # If one row is malformed, skip it but keep going. Humans make typos.
                    continue
        return loaded


# -------------------------
# Small interactive UI for humans
# -------------------------
def interactive_flow():
    print("Tiny stress estimator. Friendly, not clinical.")
    print("Press Enter to use sample data, or type 'csv' to load from a file, or 'manual' to type entries yourself.")
    choice = input("Choice [Enter/csv/manual]: ").strip().lower()

    if choice == "csv":
        path = input("Path to CSV file: ").strip()
        try:
            people = StressPredictor.load_people_from_csv(path)
            if not people:
                print("CSV gave no usable rows. Falling back to sample data.")
                people = SAMPLE_PEOPLE()
        except FileNotFoundError:
            print("File not found — falling back to sample data.")
            people = SAMPLE_PEOPLE()
    elif choice == "manual":
        people = []
        print("Enter people. Leave 'Name' blank to finish.")
        while True:
            name = input("Name: ").strip()
            if not name:
                break
            try:
                hr = float(input("  Avg heart rate (BPM): ").strip())
                sleep = float(input("  Sleep hours/day: ").strip())
                work = float(input("  Work hours/week: ").strip())
            except ValueError:
                print("  Bad number. Try that person again.")
                continue
            people.append(Person(name, hr, sleep, work))
    else:
        people = SAMPLE_PEOPLE()

    predictor = StressPredictor(people)
    predictor.pretty_print()

    # optional: save
    save = input("Save results to CSV? (y/N): ").strip().lower()
    if save == "y":
        outpath = input("Output filename (default results.csv): ").strip() or "results.csv"
        predictor.save_to_csv(outpath)
        print(f"Saved to {outpath} — open it in Excel or LibreOffice if you want a neat view.")


# -------------------------
# Sample data helper
# -------------------------
def SAMPLE_PEOPLE() -> List[Person]:
    # Realistic examples for quick checks
    return [
        Person("Alice", 75.0, 8.0, 40.0),
        Person("Bob", 92.5, 5.5, 65.0),
        Person("Charlie", 81.0, 7.0, 50.0),
        Person("Diana", 68.0, 9.5, 30.0),
    ]


# -------------------------
# If run as a script, do the interactive flow
# -------------------------
if __name__ == "__main__":
    try:
        interactive_flow()
    except KeyboardInterrupt:
        # Humans sometimes hit Ctrl+C. Be polite.
        print("\nAborted. Bye.")
        sys.exit(0)