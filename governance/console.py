"""
BYRD Console - Interactive Human-BYRD Communication

A REPL (Read-Eval-Print-Loop) for communicating with BYRD.
Enables bidirectional communication and directed self-development.

Usage:
    python -m governance.console

Commands:
    /status         - Show BYRD status
    /priorities     - Show/set domain priorities
    /desires        - List pending desires
    /inject <text>  - Inject a new desire
    /constrain <x>  - Add a constraint
    /approve        - Approve pending actions
    /reject         - Reject pending actions
    /focus <domain> - Set high priority for domain
    /help           - Show help
    /quit           - Exit console

Or just type naturally to talk with BYRD.
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from governance.director import Director, create_director

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def print_header():
    """Print BYRD console header."""
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║    ██████╗ ██╗   ██╗██████╗ ██████╗     Console                      ║
║    ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗                                 ║
║    ██████╔╝ ╚████╔╝ ██████╔╝██║  ██║    Human-BYRD Governance         ║
║    ██╔══██╗  ╚██╔╝  ██╔══██╗██║  ██║    Interface                     ║
║    ██████╔╝   ██║   ██║  ██║██████╔╝                                  ║
║    ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═════╝                                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}You are the Director. BYRD is the CEO.
Set strategy, approve decisions, provide feedback.
Type /help for commands or just talk naturally.{Colors.RESET}
""")


def print_byrd(text: str):
    """Print BYRD's response."""
    print(f"\n{Colors.GREEN}BYRD:{Colors.RESET} {text}")


def print_system(text: str):
    """Print system message."""
    print(f"\n{Colors.DIM}[{text}]{Colors.RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"\n{Colors.RED}Error: {text}{Colors.RESET}")


def show_help():
    """Show help information."""
    print(f"""
{Colors.YELLOW}Commands:{Colors.RESET}
  {Colors.BOLD}/status{Colors.RESET}           Show BYRD status and metrics
  {Colors.BOLD}/priorities{Colors.RESET}       Show current domain priorities
  {Colors.BOLD}/focus <domain>{Colors.RESET}   Set high priority for a domain
  {Colors.BOLD}/desires{Colors.RESET}          List pending desires
  {Colors.BOLD}/inject <text>{Colors.RESET}    Inject a new desire for BYRD
  {Colors.BOLD}/constrain <x>{Colors.RESET}    Add a constraint on behavior
  {Colors.BOLD}/approve{Colors.RESET}          Approve pending actions
  {Colors.BOLD}/reject{Colors.RESET}           Reject pending actions
  {Colors.BOLD}/feedback{Colors.RESET}         Provide feedback on BYRD's work
  {Colors.BOLD}/context{Colors.RESET}          Show governance context for BYRD
  {Colors.BOLD}/clear{Colors.RESET}            Clear screen
  {Colors.BOLD}/help{Colors.RESET}             Show this help
  {Colors.BOLD}/quit{Colors.RESET}             Exit console

{Colors.YELLOW}Natural Language:{Colors.RESET}
  Just type normally to talk with BYRD.
  Examples:
    "What are you currently working on?"
    "Focus on improving coding capabilities"
    "I want you to learn web search"
    "Good job on that last improvement"

{Colors.YELLOW}Philosophy:{Colors.RESET}
  You set WHAT. BYRD discovers HOW.
  You guide strategy. BYRD executes autonomously.
  Emergence is preserved. Direction is enabled.
""")


async def handle_command(director: Director, command: str, args: str) -> bool:
    """
    Handle a slash command.

    Returns:
        True if should continue, False if should exit
    """
    if command == "quit" or command == "exit":
        print_system("Goodbye. BYRD will continue to pursue the goals you've set.")
        return False

    elif command == "help":
        show_help()

    elif command == "clear":
        os.system('clear' if os.name == 'posix' else 'cls')
        print_header()

    elif command == "status":
        print(f"\n{Colors.CYAN}=== BYRD Status ==={Colors.RESET}")

        if director.byrd:
            try:
                status = await director.byrd.get_status()
                for key, value in status.items():
                    if key == "rsi_metrics":
                        print(f"\n{Colors.YELLOW}RSI Metrics:{Colors.RESET}")
                        for mk, mv in value.items():
                            print(f"  {mk}: {mv}")
                    else:
                        color = Colors.GREEN if value else Colors.RED
                        print(f"  {key}: {color}{value}{Colors.RESET}")
            except Exception as e:
                print_error(f"Could not get BYRD status: {e}")
        else:
            print(f"  {Colors.DIM}BYRD not connected{Colors.RESET}")

        print(f"\n{Colors.YELLOW}Governance:{Colors.RESET}")
        print(f"  Priorities: {len(director.priorities)}")
        print(f"  Pending desires: {len(director.pending_desires)}")
        print(f"  Active constraints: {len(director.active_constraints)}")
        print(f"  Pending approvals: {len(director.get_pending_approvals())}")

    elif command == "priorities":
        print(f"\n{Colors.CYAN}=== Domain Priorities ==={Colors.RESET}")
        if director.priorities:
            for domain, priority in sorted(director.priorities.items(),
                                          key=lambda x: x[1], reverse=True):
                bar = "█" * int(priority * 10) + "░" * (10 - int(priority * 10))
                color = Colors.GREEN if priority > 0.7 else (Colors.YELLOW if priority > 0.3 else Colors.DIM)
                print(f"  {domain:15} {color}{bar}{Colors.RESET} {priority:.1f}")
        else:
            print(f"  {Colors.DIM}No priorities set. Use /focus <domain> to set.{Colors.RESET}")

    elif command == "focus":
        if not args:
            print_error("Usage: /focus <domain>")
        else:
            director.set_priority(args.strip(), 0.9)
            print_byrd(f"Understood. I will prioritize '{args.strip()}' development.")

    elif command == "desires":
        print(f"\n{Colors.CYAN}=== Pending Desires ==={Colors.RESET}")
        if director.pending_desires:
            for i, desire in enumerate(director.pending_desires):
                print(f"  [{desire.urgency:.1f}] {desire.content}")
        else:
            print(f"  {Colors.DIM}No pending desires. Use /inject <text> to add.{Colors.RESET}")

    elif command == "inject":
        if not args:
            print_error("Usage: /inject <desire text>")
        else:
            director.inject_desire(args.strip(), urgency=0.7)
            print_byrd(f"I understand. I will pursue: '{args.strip()}'")

    elif command == "constrain":
        if not args:
            print_error("Usage: /constrain <constraint text>")
        else:
            director.add_constraint(args.strip())
            print_byrd(f"Constraint noted: '{args.strip()}'")

    elif command == "approve":
        pending = director.get_pending_approvals()
        if not pending:
            print(f"\n{Colors.DIM}No actions awaiting approval.{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}Approving {len(pending)} action(s):{Colors.RESET}")
            for approval in pending:
                director.approve(approval["id"])
                print(f"  ✓ {approval['action']}")
            print_byrd("Thank you. Proceeding with approved actions.")

    elif command == "reject":
        pending = director.get_pending_approvals()
        if not pending:
            print(f"\n{Colors.DIM}No actions awaiting approval.{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}Rejecting {len(pending)} action(s):{Colors.RESET}")
            for approval in pending:
                director.reject(approval["id"])
                print(f"  ✗ {approval['action']}")
            print_byrd("Understood. I will not proceed with those actions.")

    elif command == "feedback":
        print(f"\n{Colors.DIM}Type your feedback (or just provide it naturally):{Colors.RESET}")

    elif command == "context":
        print(f"\n{Colors.CYAN}=== Governance Context (injected into BYRD) ==={Colors.RESET}")
        context = director.get_governance_context()
        if context.strip():
            print(context)
        else:
            print(f"  {Colors.DIM}No governance context set.{Colors.RESET}")

    else:
        print_error(f"Unknown command: /{command}. Type /help for help.")

    return True


async def console_loop(director: Director):
    """Main console loop."""
    print_header()

    while True:
        try:
            # Show prompt
            print(f"\n{Colors.BLUE}Director>{Colors.RESET} ", end="", flush=True)

            # Read input
            try:
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
            except EOFError:
                print_system("EOF received. Exiting.")
                break

            user_input = user_input.strip()
            if not user_input:
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                parts = user_input[1:].split(" ", 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                should_continue = await handle_command(director, command, args)
                if not should_continue:
                    break

            else:
                # Natural language - use the say() method
                response = await director.say(user_input)
                print_byrd(response.content)

                # Show if approval is required
                if response.requires_approval:
                    print(f"\n{Colors.YELLOW}[Awaiting your response]{Colors.RESET}")

        except KeyboardInterrupt:
            print("\n")
            print_system("Use /quit to exit.")
            continue
        except Exception as e:
            print_error(f"Error: {e}")
            continue


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="BYRD Console - Human-BYRD Governance Interface")
    parser.add_argument("--connect", action="store_true",
                       help="Try to connect to running BYRD instance")
    args = parser.parse_args()

    # Create director
    byrd = None

    if args.connect:
        try:
            # Try to connect to BYRD
            from byrd import BYRD
            import yaml

            config_path = Path(__file__).parent.parent / "config.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    config = yaml.safe_load(f)

                byrd = BYRD(config)
                await byrd.start()
                print_system("Connected to BYRD instance")
        except Exception as e:
            print_system(f"Could not connect to BYRD: {e}")
            print_system("Running in standalone mode")

    director = create_director(byrd)

    try:
        await console_loop(director)
    finally:
        if byrd:
            await byrd.stop()


if __name__ == "__main__":
    asyncio.run(main())
