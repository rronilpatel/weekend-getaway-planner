#!/usr/bin/env python
import sys
import argparse
import json
from datetime import datetime

from weekend_getaway_planner.crew import WeekendGetawayPlanner

# Suppress unnecessary warnings (keep if you had issues with pysbd or similar)
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Weekend Getaway Planner CrewAI project")
    parser.add_argument("--home-city", default="Halifax, Nova Scotia",
                        help="Starting city (default: Halifax, Nova Scotia)")
    parser.add_argument("--budget", default="medium ($400–800 CAD total)",
                        help="Budget level (e.g. low, medium, high, or range like $300–600)")
    parser.add_argument("--interests", default="nature, seafood, relaxing",
                        help="Comma-separated interests (e.g. adventure, foodie, culture, relaxing)")
    parser.add_argument("--verbose", action="store_true",
                        help="Increase output verbosity")
    return parser.parse_args()


def get_inputs(args):
    """Prepare inputs dictionary for the crew"""
    return {
        "home_city": args.home_city.strip(),
        "budget": args.budget.strip(),
        "interests": args.interests.strip(),
        # Optional: you can add current_date if agents need to know season
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }


def run():
    """
    Run the Weekend Getaway Planner crew with user-provided or default inputs.
    """
    args = parse_arguments()

    inputs = get_inputs(args)

    print("Starting Weekend Getaway Planner")
    print(f"Inputs:")
    print(f"  Home city:   {inputs['home_city']}")
    print(f"  Budget:      {inputs['budget']}")
    print(f"  Interests:   {inputs['interests']}")
    print("-" * 60)

    try:
        result = WeekendGetawayPlanner().crew().kickoff(inputs=inputs)
        print("\n" + "="*80)
        print("Final Weekend Getaway Plan:")
        print(result)
        print("="*80)
    except Exception as e:
        print(f"\nError running the crew: {e}", file=sys.stderr)
        sys.exit(1)


def train():
    """
    Train the crew (placeholder — adapt if you plan to use training).
    """
    args = parse_arguments()
    inputs = get_inputs(args)

    try:
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 5
        filename = sys.argv[2] if len(sys.argv) > 2 else "training_results.json"
        print(f"Training crew for {n_iterations} iterations → saving to {filename}")
        WeekendGetawayPlanner().crew().train(
            n_iterations=n_iterations,
            filename=filename,
            inputs=inputs
        )
    except Exception as e:
        print(f"Error during training: {e}", file=sys.stderr)
        sys.exit(1)


def replay():
    """
    Replay a previous crew execution from a specific task ID.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py replay <task_id>", file=sys.stderr)
        sys.exit(1)

    try:
        task_id = sys.argv[1]
        print(f"Replaying task: {task_id}")
        WeekendGetawayPlanner().crew().replay(task_id=task_id)
    except Exception as e:
        print(f"Error replaying: {e}", file=sys.stderr)
        sys.exit(1)


def test():
    """
    Test the crew execution (placeholder — adapt as needed).
    """
    args = parse_arguments()
    inputs = get_inputs(args)

    try:
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        eval_llm = sys.argv[2] if len(sys.argv) > 2 else "gpt-4o-mini"
        print(f"Testing crew for {n_iterations} iterations with eval LLM: {eval_llm}")
        WeekendGetawayPlanner().crew().test(
            n_iterations=n_iterations,
            eval_llm=eval_llm,
            inputs=inputs
        )
    except Exception as e:
        print(f"Error during testing: {e}", file=sys.stderr)
        sys.exit(1)


def run_with_trigger():
    """
    Run the crew with a JSON trigger payload (for webhooks, etc.).
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py run_with_trigger '<json_payload>'", file=sys.stderr)
        sys.exit(1)

    try:
        trigger_payload = json.loads(sys.argv[1])
        inputs = {
            "crewai_trigger_payload": trigger_payload,
            "home_city": trigger_payload.get("home_city", "Halifax, Nova Scotia"),
            "budget": trigger_payload.get("budget", "medium"),
            "interests": trigger_payload.get("interests", "relaxing, nature"),
        }
        print("Running crew with trigger payload")
        result = WeekendGetawayPlanner().crew().kickoff(inputs=inputs)
        print(result)
    except json.JSONDecodeError:
        print("Invalid JSON payload", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running with trigger: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["train", "replay", "test", "run_with_trigger"]:
        globals()[sys.argv[1]]()
    else:
        run()
