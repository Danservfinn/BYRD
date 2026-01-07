#!/usr/bin/env python3
"""
Talk to BYRD - Simple Interactive Interface

A simple way to communicate with BYRD and direct its development.

Usage:
    python talk_to_byrd.py              # Start interactive console
    python talk_to_byrd.py --status     # Show current status
    python talk_to_byrd.py --inject "Improve coding skills"  # Inject a desire

This provides a human-friendly interface for the governance system.
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from governance.director import Director, create_director
from governance.direction_file import DirectionFile


def simple_repl():
    """Simple synchronous REPL for quick interactions."""
    director = create_director()
    direction_file = DirectionFile()

    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                     BYRD - Interactive Console                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  You are the Director. Guide BYRD's development.                      ║
║                                                                       ║
║  Commands:                                                            ║
║    focus <domain>    - Prioritize a domain (coding, reasoning, etc)   ║
║    want <desire>     - Tell BYRD what you want                        ║
║    status            - Show current state                             ║
║    priorities        - Show domain priorities                         ║
║    help              - Show all commands                              ║
║    quit              - Exit                                           ║
║                                                                       ║
║  Or just type naturally to communicate with BYRD.                     ║
╚═══════════════════════════════════════════════════════════════════════╝
""")

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue

            # Parse command
            parts = user_input.split(" ", 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command in ["quit", "exit", "q"]:
                print("\nGoodbye. BYRD will continue pursuing your goals.")
                break

            elif command == "help":
                print("""
Commands:
  focus <domain>     - Set high priority for a domain
                       Example: focus coding

  want <text>        - Inject a desire for BYRD to pursue
                       Example: want Improve SWE-bench score to 60%

  constrain <text>   - Add a constraint on behavior
                       Example: constrain Do not modify production code

  status             - Show current governance state

  priorities         - Show domain priorities

  file               - Show path to direction file (for async edits)

  read               - Read current direction file

  help               - Show this help

  quit               - Exit console

Natural language:
  Just type naturally and BYRD will interpret your intent.
  Examples:
    "I want you to focus on reasoning capabilities"
    "What's your current status?"
    "Good job on that improvement"
""")

            elif command == "focus":
                if not args:
                    print("Usage: focus <domain>")
                    print("Domains: coding, reasoning, economic, creative, planning")
                else:
                    director.set_priority(args.strip(), 0.9)
                    print(f"\nBYRD: I'll prioritize '{args.strip()}' development.")

            elif command == "want" or command == "desire":
                if not args:
                    print("Usage: want <desire text>")
                else:
                    director.inject_desire(args.strip(), urgency=0.7)
                    print(f"\nBYRD: I understand. I'll pursue: '{args.strip()}'")

            elif command == "constrain":
                if not args:
                    print("Usage: constrain <constraint text>")
                else:
                    director.add_constraint(args.strip())
                    print(f"\nBYRD: Constraint noted: '{args.strip()}'")

            elif command == "status":
                print("\n=== BYRD Governance State ===")
                print(f"\nPriorities:")
                if director.priorities:
                    for domain, priority in sorted(director.priorities.items(),
                                                  key=lambda x: x[1], reverse=True):
                        bar = "█" * int(priority * 10) + "░" * (10 - int(priority * 10))
                        print(f"  {domain:15} {bar} {priority:.1f}")
                else:
                    print("  (none set)")

                print(f"\nPending Desires: {len(director.pending_desires)}")
                for d in director.pending_desires[:3]:
                    print(f"  [{d.urgency:.1f}] {d.content}")

                print(f"\nActive Constraints: {len(director.active_constraints)}")
                for c in director.active_constraints[:3]:
                    print(f"  - {c.content}")

                print(f"\nPending Approvals: {len(director.get_pending_approvals())}")

            elif command == "priorities":
                print("\n=== Domain Priorities ===")
                if director.priorities:
                    for domain, priority in sorted(director.priorities.items(),
                                                  key=lambda x: x[1], reverse=True):
                        bar = "█" * int(priority * 10) + "░" * (10 - int(priority * 10))
                        print(f"  {domain:15} {bar} {priority:.1f}")
                else:
                    print("  No priorities set. Use 'focus <domain>' to set.")

            elif command == "file":
                print(f"\nDirection file: {direction_file.direction_file.absolute()}")
                print("Edit this file to provide async direction to BYRD.")

            elif command == "read":
                direction = direction_file.read_direction()
                print("\n=== Current Direction File ===")
                print(f"Priorities: {direction['priorities']}")
                print(f"Desires: {direction['desires']}")
                print(f"Constraints: {direction['constraints']}")
                print(f"Feedback: {direction['feedback']}")

            else:
                # Natural language - interpret as desire or question
                response = asyncio.run(director.say(user_input))
                print(f"\nBYRD: {response.content}")

        except KeyboardInterrupt:
            print("\n\nUse 'quit' to exit.")
        except EOFError:
            print("\n\nGoodbye.")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Talk to BYRD - Interactive Human-BYRD Communication"
    )
    parser.add_argument("--status", action="store_true",
                       help="Show current governance status")
    parser.add_argument("--inject", type=str,
                       help="Inject a desire and exit")
    parser.add_argument("--focus", type=str,
                       help="Set a domain priority and exit")
    parser.add_argument("--file", action="store_true",
                       help="Show direction file path")

    args = parser.parse_args()

    director = create_director()
    direction_file = DirectionFile()

    if args.status:
        print("=== BYRD Governance State ===")
        print(f"\nPriorities: {director.priorities}")
        print(f"Pending Desires: {len(director.pending_desires)}")
        print(f"Active Constraints: {len(director.active_constraints)}")
        print(f"\nDirection File: {direction_file.direction_file}")

    elif args.inject:
        director.inject_desire(args.inject, urgency=0.7)
        print(f"Injected desire: {args.inject}")

    elif args.focus:
        director.set_priority(args.focus, 0.9)
        print(f"Set priority: {args.focus} = 0.9")

    elif args.file:
        print(f"Direction file: {direction_file.direction_file.absolute()}")
        print("\nEdit this file to provide direction to BYRD.")

    else:
        # Start interactive REPL
        simple_repl()


if __name__ == "__main__":
    main()
