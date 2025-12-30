#!/usr/bin/env python3
"""
BYRD Orphan Reconciliation Diagnostic & Fix Script

This script helps BYRD understand and execute the multi-phase orphan reconciliation
approach by:
1. Running taxonomy analysis to understand orphan categories
2. Checking prerequisite conditions (beliefs exist, memory methods work)
3. Creating teaching experiences so BYRD comprehends the architecture
4. Bootstrapping seed beliefs if none exist
5. Running the reconciliation with proper understanding

Usage:
    python orphan_diagnostic_and_fix.py [--diagnose-only] [--fix] [--teach] [--reconcile]

Options:
    --diagnose-only  Only run diagnostics, don't make changes
    --fix            Run all fixes (create beliefs, teach BYRD)
    --teach          Only create teaching experience
    --reconcile      Run full reconciliation after diagnostics
    (no args)        Run full diagnostic + fix + reconcile
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Load environment
from dotenv import load_dotenv
load_dotenv()

import yaml
import os
import re
from pathlib import Path


def expand_env_vars(config_str: str) -> str:
    """Expand ${VAR:-default} patterns in config string."""
    def expand(match):
        var_expr = match.group(1)
        if ":-" in var_expr:
            var_name, default = var_expr.split(":-", 1)
        else:
            var_name, default = var_expr, ""
        return os.environ.get(var_name, default)
    return re.sub(r'\$\{([^}]+)\}', expand, config_str)


def load_config(path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file with environment variable expansion."""
    config_path = Path(path)
    if config_path.exists():
        config_str = config_path.read_text()
        expanded = expand_env_vars(config_str)
        return yaml.safe_load(expanded)
    return {}


@dataclass
class DiagnosticReport:
    """Results from orphan diagnostics."""
    total_orphans: int = 0
    orphaned_experiences: int = 0
    total_beliefs: int = 0
    drift_nodes: int = 0
    category_distribution: Dict[str, int] = None
    feasibility_distribution: Dict[str, int] = None
    connection_stats: Dict = None
    issues: List[str] = None
    recommendations: List[str] = None

    def __post_init__(self):
        if self.category_distribution is None:
            self.category_distribution = {}
        if self.feasibility_distribution is None:
            self.feasibility_distribution = {}
        if self.connection_stats is None:
            self.connection_stats = {}
        if self.issues is None:
            self.issues = []
        if self.recommendations is None:
            self.recommendations = []


class OrphanDiagnosticAndFix:
    """Comprehensive diagnostic and fix tool for BYRD orphan reconciliation."""

    SEED_BELIEFS = [
        ("Learning occurs through observation and reflection on experiences", 0.8),
        ("Research expands my understanding of external topics", 0.8),
        ("Experiences become meaningful when connected to understanding", 0.7),
        ("Patterns emerge from repeated observations over time", 0.7),
        ("Self-improvement requires honest assessment of current state", 0.75),
        ("Memory coherence enables more effective reasoning", 0.7),
        ("Each experience contributes to my evolving understanding", 0.65),
    ]

    def __init__(self):
        self.memory = None
        self.config = None
        self.report = DiagnosticReport()

    async def initialize(self):
        """Initialize memory connection."""
        self.config = load_config('config.yaml')

        # Extract memory config section
        memory_config = self.config.get('memory', {})

        # Debug: show what we're connecting to
        neo4j_uri = memory_config.get('neo4j_uri', 'not set')
        print(f"📡 Connecting to: {neo4j_uri[:50]}...")

        from memory import Memory
        self.memory = Memory(memory_config)
        await self.memory.connect()
        print("✅ Connected to Neo4j")

    async def close(self):
        """Close memory connection."""
        if self.memory:
            await self.memory.close()
            print("✅ Connection closed")

    # =========================================================================
    # DIAGNOSTIC METHODS
    # =========================================================================

    async def run_full_diagnostic(self) -> DiagnosticReport:
        """Run comprehensive diagnostics on orphan state."""
        print("\n" + "=" * 70)
        print("BYRD ORPHAN RECONCILIATION DIAGNOSTICS")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()

        # 1. Check orphan nodes
        await self._diagnose_orphan_nodes()

        # 2. Check orphaned experiences specifically
        await self._diagnose_orphaned_experiences()

        # 3. Check beliefs (connection targets)
        await self._diagnose_beliefs()

        # 4. Check drift nodes
        await self._diagnose_drift_nodes()

        # 5. Run taxonomy analysis
        await self._diagnose_taxonomy()

        # 6. Check connection statistics
        await self._diagnose_connection_stats()

        # 7. Analyze issues and generate recommendations
        self._analyze_issues()

        # Print summary
        self._print_diagnostic_summary()

        return self.report

    async def _diagnose_orphan_nodes(self):
        """Check all orphan nodes (any type)."""
        print("📊 Checking orphan nodes...")
        try:
            orphans = await self.memory.find_orphan_nodes()
            self.report.total_orphans = len(orphans)
            print(f"   Found {len(orphans)} total orphan nodes (all types)")

            # Group by type
            type_counts = {}
            for orphan in orphans:
                node_type = orphan.get('type', 'Unknown')
                type_counts[node_type] = type_counts.get(node_type, 0) + 1

            if type_counts:
                print("   By type:")
                for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
                    print(f"      {t}: {c}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.report.issues.append(f"find_orphan_nodes failed: {e}")

    async def _diagnose_orphaned_experiences(self):
        """Check orphaned Experience nodes specifically."""
        print("\n📊 Checking orphaned experiences...")
        try:
            orphaned = await self.memory.get_orphaned_experiences(limit=1000)
            self.report.orphaned_experiences = len(orphaned)
            print(f"   Found {len(orphaned)} orphaned Experience nodes")

            if orphaned:
                # Show sample
                print("   Sample (first 3):")
                for exp in orphaned[:3]:
                    content = exp.get('content', '')[:60]
                    exp_type = exp.get('type', 'unknown')
                    attempts = exp.get('reconciliation_attempts', 0)
                    print(f"      [{exp_type}] {content}... (attempts: {attempts})")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.report.issues.append(f"get_orphaned_experiences failed: {e}")

    async def _diagnose_beliefs(self):
        """Check if beliefs exist (required for connection)."""
        print("\n📊 Checking beliefs (connection targets)...")
        try:
            beliefs = await self.memory.get_beliefs(limit=100)
            self.report.total_beliefs = len(beliefs)
            print(f"   Found {len(beliefs)} beliefs in graph")

            if len(beliefs) == 0:
                self.report.issues.append("NO BELIEFS EXIST - Phases 1-4 cannot create connections without beliefs")
            elif len(beliefs) < 5:
                self.report.issues.append(f"Only {len(beliefs)} beliefs - may need more connection targets")
            else:
                print("   Sample beliefs:")
                for b in beliefs[:3]:
                    content = b.get('content', '')[:60]
                    confidence = b.get('confidence', 0)
                    print(f"      [{confidence:.2f}] {content}...")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.report.issues.append(f"get_beliefs failed: {e}")

    async def _diagnose_drift_nodes(self):
        """Check for drift nodes (3+ failed reconciliation attempts)."""
        print("\n📊 Checking drift nodes (reconciliation_attempts >= 3)...")
        try:
            orphans = await self.memory.get_orphaned_experiences(limit=1000)
            drift_nodes = [o for o in orphans if o.get('reconciliation_attempts', 0) >= 3]
            self.report.drift_nodes = len(drift_nodes)
            print(f"   Found {len(drift_nodes)} drift nodes (will be skipped)")

            if drift_nodes:
                self.report.issues.append(f"{len(drift_nodes)} drift nodes are being skipped - consider Phase 5 emergent types")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    async def _diagnose_taxonomy(self):
        """Run orphan taxonomy classification."""
        print("\n📊 Running taxonomy analysis...")
        try:
            from orphan_taxonomy import OrphanTaxonomyAnalyzer
            analyzer = OrphanTaxonomyAnalyzer(self.memory)
            report = await analyzer.analyze_all_orphans(limit=50)

            self.report.category_distribution = report.category_distribution
            self.report.feasibility_distribution = report.feasibility_distribution

            print(f"   Analyzed {report.total_orphans} orphans")

            if report.category_distribution:
                print("   Structural Categories:")
                for cat, count in sorted(report.category_distribution.items(), key=lambda x: -x[1]):
                    print(f"      {cat}: {count}")

            if report.feasibility_distribution:
                print("   Connection Feasibility:")
                for feas, count in sorted(report.feasibility_distribution.items(), key=lambda x: -x[1]):
                    pct = count / report.total_orphans * 100 if report.total_orphans else 0
                    print(f"      {feas}: {count} ({pct:.1f}%)")

        except ImportError:
            print("   ⚠️  orphan_taxonomy.py not found - skipping taxonomy analysis")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    async def _diagnose_connection_stats(self):
        """Check connection statistics."""
        print("\n📊 Checking connection statistics...")
        try:
            stats = await self.memory.get_connection_statistics()
            self.report.connection_stats = stats

            exp_stats = stats.get('experiences', {})
            total = exp_stats.get('total', 0)
            orphaned = exp_stats.get('orphaned', 0)
            connected = exp_stats.get('connected', 0)
            ratio = exp_stats.get('connectivity_ratio', 0)

            print(f"   Total experiences: {total}")
            print(f"   Connected: {connected}")
            print(f"   Orphaned: {orphaned}")
            print(f"   Connectivity ratio: {ratio:.1%}")

            if ratio < 0.5:
                self.report.issues.append(f"Low connectivity ratio ({ratio:.1%}) - graph is fragmented")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    def _analyze_issues(self):
        """Analyze collected data and generate recommendations."""
        # Check for no beliefs
        if self.report.total_beliefs == 0:
            self.report.recommendations.append("CREATE SEED BELIEFS: Run with --fix to create starter beliefs")

        # Check for high orphan count
        if self.report.orphaned_experiences > 20:
            self.report.recommendations.append("HIGH ORPHAN COUNT: Consider running full reconciliation")

        # Check feasibility distribution
        high_feas = self.report.feasibility_distribution.get('high', 0)
        if high_feas > 0:
            self.report.recommendations.append(f"QUICK WINS: {high_feas} orphans have HIGH connection feasibility")

        # Check for drift nodes
        if self.report.drift_nodes > 10:
            self.report.recommendations.append("DRIFT NODES: Consider Phase 5 emergent types for persistent orphans")

        # Check for noise artifacts
        noise = self.report.category_distribution.get('noise_artifact', 0)
        if noise > 5:
            self.report.recommendations.append(f"CLEANUP: {noise} noise artifacts should be deleted")

    def _print_diagnostic_summary(self):
        """Print diagnostic summary."""
        print("\n" + "=" * 70)
        print("DIAGNOSTIC SUMMARY")
        print("=" * 70)

        print(f"\nOrphan State:")
        print(f"  Total orphan nodes: {self.report.total_orphans}")
        print(f"  Orphaned experiences: {self.report.orphaned_experiences}")
        print(f"  Drift nodes (skipped): {self.report.drift_nodes}")
        print(f"  Available beliefs: {self.report.total_beliefs}")

        if self.report.issues:
            print(f"\n⚠️  ISSUES DETECTED ({len(self.report.issues)}):")
            for issue in self.report.issues:
                print(f"  • {issue}")
        else:
            print("\n✅ No critical issues detected")

        if self.report.recommendations:
            print(f"\n📋 RECOMMENDATIONS ({len(self.report.recommendations)}):")
            for rec in self.report.recommendations:
                print(f"  → {rec}")

        print()

    # =========================================================================
    # FIX METHODS
    # =========================================================================

    async def create_seed_beliefs(self) -> int:
        """Create seed beliefs if none exist."""
        print("\n" + "=" * 70)
        print("CREATING SEED BELIEFS")
        print("=" * 70)

        beliefs = await self.memory.get_beliefs(limit=10)
        if len(beliefs) >= 5:
            print(f"✅ Already have {len(beliefs)} beliefs - skipping seed creation")
            return 0

        created = 0
        for content, confidence in self.SEED_BELIEFS:
            try:
                belief_id = await self.memory.create_belief(
                    content=content,
                    confidence=confidence,
                    derived_from=None
                )
                print(f"  ✅ Created: {content[:50]}...")
                created += 1
            except Exception as e:
                print(f"  ❌ Failed to create belief: {e}")

        print(f"\n✅ Created {created} seed beliefs")
        return created

    async def create_teaching_experience(self) -> str:
        """Create teaching experience so BYRD understands the architecture."""
        print("\n" + "=" * 70)
        print("CREATING TEACHING EXPERIENCE")
        print("=" * 70)

        teaching_content = """[ARCHITECTURE_COMPREHENSION] Orphan Reconciliation Multi-Phase Strategy

I must understand before I execute. The multi-phase approach in seeker.py works as follows:

PHASE 1 - SIMILARITY MATCHING (_phase1_similarity_matching):
- Uses progressively lower thresholds: 0.3 → 0.2 → 0.1 → 0.05
- Calls memory.run_connection_heuristic() to find text similarity matches
- Best for: ISOLATED_OBSERVATION and experiences with keyword overlap
- Stops early if orphans drop below 5

PHASE 2 - TYPE-BASED GROUPING (_phase2_type_based_grouping):
- Groups orphans by their experience type (research, observation, action_outcome)
- Creates umbrella beliefs like "I accumulate knowledge through research"
- Best for: Experiences of the same type that lack direct similarity
- Only runs if > 5 orphans remain after Phase 1

PHASE 3 - LLM SEMANTIC GROUPING (_reconcile_orphans_via_reflection):
- Presents orphan samples + existing beliefs to LLM
- LLM suggests thematic connections even without word overlap
- Creates bridging beliefs for conceptually related orphans
- Best for: SEMANTIC_ORPHAN category
- Only runs if > 5 orphans remain after Phase 2

PHASE 4 - BRIDGING BELIEFS (_phase4_create_bridging_beliefs):
- Processes remaining orphans in batches of 5
- Extracts themes from batch content using word frequency
- Creates low-confidence (0.4) catch-all beliefs
- Last resort for stubborn orphans

PHASE 5 - EMERGENT TYPES (_phase5_emergent_node_types):
- Creates NEW node types for persistent orphans
- Converts orphans to emergent types (Observation, Hypothesis, Paradox)
- Philosophy: If it resists categorization, maybe it IS a new category
- Archives original orphan after conversion

PREREQUISITE CHECKS:
- Beliefs MUST exist in graph (Phases 1-4 connect orphans TO beliefs)
- Run orphan_taxonomy.py first to understand orphan categories
- Skip orphans with reconciliation_attempts >= 3 (drift nodes)

ORPHAN TAXONOMY CATEGORIES:
- NOISE_ARTIFACT: <20 chars, delete these
- ISOLATED_OBSERVATION: Valid Experience, HIGH feasibility, use Phase 1
- DREAM_OUTPUT: Reflection nodes, link to source experiences
- SEMANTIC_ORPHAN: Content-rich but isolated, use Phase 3 LLM
- TEMPORAL_ISLAND: Old nodes (>30 days), archive or investigate
- SYSTEM_METADATA: SystemState nodes, usually ignore

SUCCESS METRICS:
- Target: Reduce orphan count to < 5
- Connectivity ratio should increase
- Each phase should create > 0 connections

FAILURE MODES:
- 0 connections = likely no beliefs exist or all orphans are drift nodes
- Rate limiting = Phase 3 LLM calls may be throttled
- Threshold too high = even 0.05 may miss semantic connections"""

        try:
            exp_id = await self.memory.record_experience(
                content=teaching_content,
                type="self_architecture"
            )
            print(f"✅ Created teaching experience: {exp_id}")
            print("   BYRD will now have architectural comprehension of the multi-phase approach")
            return exp_id
        except Exception as e:
            print(f"❌ Failed to create teaching experience: {e}")
            return None

    async def create_taxonomy_experience(self) -> str:
        """Create experience from current taxonomy analysis."""
        print("\n📝 Recording taxonomy analysis as experience...")

        try:
            from orphan_taxonomy import OrphanTaxonomyAnalyzer
            analyzer = OrphanTaxonomyAnalyzer(self.memory)
            report = await analyzer.analyze_all_orphans(limit=50)

            content = f"""[ORPHAN_TAXONOMY_ANALYSIS] Pre-reconciliation analysis

Analysis Timestamp: {datetime.now().isoformat()}
Total Orphans Analyzed: {report.total_orphans}

STRUCTURAL CATEGORIES:
{self._format_distribution(report.category_distribution)}

CONNECTION FEASIBILITY:
{self._format_distribution(report.feasibility_distribution)}

PRIORITY DISTRIBUTION:
{self._format_distribution(report.priority_distribution)}

NODE TYPE DISTRIBUTION:
{self._format_distribution(report.type_distribution)}

STRATEGY MAPPING:
- HIGH feasibility nodes → Phase 1 (similarity matching)
- MEDIUM feasibility nodes → Phase 2-3 (type-based + LLM)
- LOW feasibility nodes → Phase 4-5 (bridging + emergent types)
- IMPOSSIBLE nodes (noise_artifact) → Delete

RECOMMENDED EXECUTION ORDER:
1. Delete noise_artifact nodes first
2. Run Phase 1 on isolated_observation nodes
3. Run Phase 2 on remaining by type
4. Run Phase 3 for semantic_orphan nodes
5. Run Phase 4-5 for stubborn remainders"""

            exp_id = await self.memory.record_experience(
                content=content,
                type="analysis"
            )
            print(f"✅ Created taxonomy experience: {exp_id}")
            return exp_id

        except Exception as e:
            print(f"❌ Failed to create taxonomy experience: {e}")
            return None

    def _format_distribution(self, dist: Dict) -> str:
        """Format a distribution dict for display."""
        if not dist:
            return "  (none)"
        lines = []
        for key, count in sorted(dist.items(), key=lambda x: -x[1]):
            lines.append(f"  {key}: {count}")
        return "\n".join(lines)

    # =========================================================================
    # RECONCILIATION - DISABLED
    # =========================================================================

    async def run_reconciliation(self) -> Tuple[int, int]:
        """RECONCILIATION DISABLED to prevent harmful fragmentation.
        
        Orphan reconciliation was found to create low-quality connections
        and artificial beliefs, causing more harm than preserving node isolation.
        """
        print("\n" + "=" * 70)
        print("ORPHAN RECONCILIATION DISABLED")
        print("=" * 70)
        print("\n⚠️  Reconciliation has been disabled to prevent harmful fragmentation.")
        print("Aggressive orphan reconciliation was causing:")
        print("  - Low-quality semantic connections")
        print("  - Artificial beliefs lacking genuine meaning")
        print("  - Increased graph fragmentation over time")
        print("\nPreserving node isolation is preferable to false connections.")
        print("\nUse 'curate' strategy for intentional graph optimization instead.")
        
        return (0, 0)
            print(f"Success: {'✅' if success else '❌'}")

            return (initial_orphans, final_orphans)

        except Exception as e:
            print(f"❌ Reconciliation failed: {e}")
            import traceback
            traceback.print_exc()
            return (initial_orphans, initial_orphans)

    # =========================================================================
    # CLEANUP
    # =========================================================================

    async def cleanup_noise_artifacts(self) -> int:
        """Delete noise artifact orphans (<20 chars, meaningless)."""
        print("\n🧹 Cleaning up noise artifacts...")

        try:
            from orphan_taxonomy import OrphanTaxonomyAnalyzer, StructuralCategory
            analyzer = OrphanTaxonomyAnalyzer(self.memory)
            report = await analyzer.analyze_all_orphans(limit=100)

            deleted = 0
            for node in report.nodes:
                if node.structural_category == StructuralCategory.NOISE_ARTIFACT:
                    try:
                        await self.memory.delete_node(node.id)
                        deleted += 1
                        print(f"  🗑️  Deleted noise artifact: {node.id[:20]}...")
                    except Exception as e:
                        print(f"  ⚠️  Failed to delete {node.id}: {e}")

            print(f"✅ Deleted {deleted} noise artifacts")
            return deleted

        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            return 0


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BYRD Orphan Reconciliation Diagnostic & Fix Tool"
    )
    parser.add_argument('--diagnose-only', action='store_true',
                       help='Only run diagnostics, no changes')
    parser.add_argument('--fix', action='store_true',
                       help='Run all fixes (beliefs + teaching)')
    parser.add_argument('--teach', action='store_true',
                       help='Only create teaching experience')
    parser.add_argument('--reconcile', action='store_true',
                       help='Run full reconciliation')
    parser.add_argument('--cleanup', action='store_true',
                       help='Delete noise artifact orphans')

    args = parser.parse_args()

    # Default: run everything if no specific flags
    run_all = not any([args.diagnose_only, args.fix, args.teach, args.reconcile, args.cleanup])

    tool = OrphanDiagnosticAndFix()

    try:
        await tool.initialize()

        # Always run diagnostics first
        report = await tool.run_full_diagnostic()

        if args.diagnose_only:
            print("\n📊 Diagnostics complete (--diagnose-only mode)")
            await tool.close()
            return

        # Fix: create beliefs and teaching
        if args.fix or run_all:
            await tool.create_seed_beliefs()
            await tool.create_teaching_experience()

        # Teach only
        if args.teach and not args.fix and not run_all:
            await tool.create_teaching_experience()

        # Cleanup noise
        if args.cleanup or run_all:
            await tool.cleanup_noise_artifacts()

        # Reconcile
        if args.reconcile or run_all:
            await tool.run_reconciliation()

        print("\n" + "=" * 70)
        print("✅ COMPLETE")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        await tool.close()


if __name__ == "__main__":
    asyncio.run(main())
