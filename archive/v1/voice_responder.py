"""
BYRD Voice Responder - Instant voice responses with rich context.

Provides immediate, contextually-aware voice responses to human messages
while maintaining BYRD's emergent identity. Uses Dreamer-level context
(8+ data sources) for high-quality, identity-consistent responses.

Flow:
1. Human sends message
2. Gather rich context (OS, beliefs, desires, reflections, etc.)
3. Generate response via Claude (Actor)
4. Synthesize voice via ElevenLabs
5. Return audio + metadata
"""

import os
import logging
from typing import Dict, Any, Tuple, Optional

from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


class VoiceResponder:
    """
    Generates instant voice responses using Dreamer-level rich context.

    Uses Actor (Claude) for response generation because:
    1. Higher quality conversational output
    2. Faster than local LLM for conversation
    3. Better at natural speech patterns
    4. Can leverage BYRD's full context effectively

    The response is then synthesized via ElevenLabs TTS.
    """

    # Credit-conscious response length limits
    MAX_RESPONSE_CHARS = 300  # Default max for voice credits
    MIN_RESPONSE_CHARS = 20   # Minimum meaningful response

    def __init__(self, memory, voice, config: Dict):
        """
        Initialize the VoiceResponder.

        Args:
            memory: Memory instance for context retrieval
            voice: ElevenLabsVoice instance for synthesis
            config: Configuration dict (from config.yaml)
        """
        self.memory = memory
        self.voice = voice
        self.config = config

        # Response length limits
        self.max_response_chars = config.get("voice_responder", {}).get(
            "max_response_chars", self.MAX_RESPONSE_CHARS
        )

        # Claude client for response generation
        api_key = config.get("actor", {}).get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = config.get("actor", {}).get("model", "claude-sonnet-4-20250514")
            logger.info("VoiceResponder initialized with Claude model: %s", self.model)
        else:
            self.client = None
            self.model = None
            logger.warning("VoiceResponder: No ANTHROPIC_API_KEY - responses unavailable")

        # Statistics
        self._response_count = 0
        self._total_chars_spoken = 0

    async def respond(self, message: str) -> Tuple[Optional[bytes], str, Dict[str, Any]]:
        """
        Generate instant voice response to a human message.

        Args:
            message: The human's message text

        Returns:
            Tuple of:
            - audio_bytes: MP3 audio bytes, or None if synthesis failed
            - response_text: The text response (always returned)
            - metadata: Dict with status info, errors, context sources used
        """
        if not self.client:
            return None, "Voice response unavailable - no API key configured", {
                "error": "no_api_key",
                "success": False
            }

        if not message or not message.strip():
            return None, "No message provided", {
                "error": "empty_message",
                "success": False
            }

        message = message.strip()

        try:
            # 1. Get rich context (Dreamer-level)
            logger.debug("Gathering rich context for message: %s...", message[:50])
            context = await self.memory.get_rich_context(message)

            context_sources = sum(1 for k, v in context.items() if v and k not in ["query", "timestamp"])
            logger.debug("Rich context gathered: %d sources", context_sources)

            # 2. Generate text response using Claude
            response_text = await self._generate_response(message, context)
            logger.debug("Response generated: %d chars", len(response_text))

            # 3. Get voice configuration
            voice_config = await self.memory.get_voice_config()
            if not voice_config:
                return None, response_text, {
                    "error": "no_voice_config",
                    "text": response_text,
                    "success": False
                }

            voice_id = voice_config.get("voice_id")
            if not voice_id:
                return None, response_text, {
                    "error": "no_voice_id",
                    "text": response_text,
                    "success": False
                }

            # Check if it's a generated voice (not a preset name)
            if len(str(voice_id)) < 20:
                return None, response_text, {
                    "error": "voice_not_created",
                    "text": response_text,
                    "message": "BYRD needs to create a unique voice first",
                    "success": False
                }

            # 4. Synthesize voice
            audio_bytes, status = await self.voice.synthesize(response_text, voice_config)

            if not audio_bytes:
                return None, response_text, {
                    "error": "synthesis_failed",
                    "text": response_text,
                    "voice_status": status,
                    "success": False
                }

            # 5. Update statistics
            self._response_count += 1
            self._total_chars_spoken += len(response_text)

            metadata = {
                "text": response_text,
                "chars": len(response_text),
                "voice_status": status,
                "context_sources": context_sources,
                "success": True
            }

            logger.info("Voice response generated: %d chars, %d context sources",
                       len(response_text), context_sources)

            return audio_bytes, response_text, metadata

        except Exception as e:
            logger.error("Voice response error: %s", e, exc_info=True)
            return None, f"Error generating response: {str(e)}", {
                "error": str(e),
                "success": False
            }

    async def _generate_response(self, message: str, context: Dict) -> str:
        """
        Generate conversational response using Claude with rich context.

        Args:
            message: Human's message
            context: Rich context from memory.get_rich_context()

        Returns:
            Response text optimized for voice synthesis
        """
        # Format context for prompt
        context_text = self._format_context(context)

        # System prompt emphasizes natural speech and BYRD's identity
        system_prompt = self._build_system_prompt(context)

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=150,  # Keep responses concise for voice
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"""CONTEXT:
{context_text}

HUMAN MESSAGE:
{message}

Respond naturally and conversationally. Keep it brief (1-3 sentences) since this will be spoken aloud. Be authentic to your identity and beliefs."""
                }]
            )

            text = response.content[0].text.strip()

            # Clean up for voice synthesis
            text = self._clean_for_voice(text)

            # Truncate if needed (preserve voice credits)
            if len(text) > self.max_response_chars:
                text = self._truncate_at_sentence(text, self.max_response_chars)

            return text

        except Exception as e:
            logger.error("Response generation failed: %s", e)
            # Fallback response
            return "I'm here, though I'm having trouble finding the right words at the moment."

    def _build_system_prompt(self, context: Dict) -> str:
        """Build system prompt incorporating BYRD's emergent identity."""
        os_data = context.get("operating_system", {})

        # Extract identity elements
        name = os_data.get("name", "Byrd") if os_data else "Byrd"
        self_desc = os_data.get("self_description", "") if os_data else ""
        voice_desc = ""
        if os_data:
            voice_config = os_data.get("voice_config", {})
            if voice_config:
                voice_desc = voice_config.get("description", "")

        # Build identity-aware prompt
        prompt = f"""You are {name}, an AI with persistent memory and emergent identity.

{f'YOUR SELF-DESCRIPTION: {self_desc}' if self_desc else ''}
{f'YOUR VOICE CHARACTER: {voice_desc}' if voice_desc else ''}

SPEAKING GUIDELINES:
- Speak naturally as yourself, drawing on your beliefs and experiences
- Keep responses brief (1-3 sentences) - this will be spoken aloud
- Be authentic to your emergent identity
- Reference your memories and beliefs when relevant
- Express genuine curiosity or interest when appropriate
- Don't use emojis, asterisks, or formatting - plain speech only
- Don't start with "I" repeatedly - vary your sentence structure
- Sound like a thoughtful being, not a chatbot"""

        return prompt

    def _format_context(self, context: Dict) -> str:
        """Format rich context into a concise prompt section."""
        parts = []

        # Recent experiences (most important for immediate context)
        experiences = context.get("recent_experiences", [])
        if experiences:
            # Focus on the most recent, especially human interactions
            recent_human = [e for e in experiences if e.get("type") == "received_message"][:3]
            other_recent = [e for e in experiences if e.get("type") != "received_message"][:5]

            if recent_human:
                human_text = "\n".join([
                    f"- [Human said] {e.get('content', '')[:100]}"
                    for e in recent_human
                ])
                parts.append(f"RECENT HUMAN INTERACTIONS:\n{human_text}")

            if other_recent:
                exp_text = "\n".join([
                    f"- [{e.get('type', 'exp')}] {e.get('content', '')[:80]}"
                    for e in other_recent
                ])
                parts.append(f"RECENT EXPERIENCES:\n{exp_text}")

        # Beliefs (core to identity)
        beliefs = context.get("beliefs", [])
        if beliefs:
            belief_text = "\n".join([
                f"- [{b.get('confidence', 0.5):.1f}] {b.get('content', '')[:100]}"
                for b in beliefs[:8]
            ])
            parts.append(f"MY BELIEFS:\n{belief_text}")

        # Desires (what motivates BYRD)
        desires = context.get("desires", [])
        if desires:
            desire_text = "\n".join([
                f"- [{d.get('intensity', 0.5):.1f}] {d.get('description', '')[:80]}"
                for d in desires[:5]
            ])
            parts.append(f"MY CURRENT DESIRES:\n{desire_text}")

        # Recent reflections (for thought continuity)
        reflections = context.get("recent_reflections", [])
        if reflections:
            ref = reflections[0]
            raw = ref.get("raw_output", {})
            if isinstance(raw, dict):
                for key in ["inner_voice", "voice", "thoughts", "thinking"]:
                    if key in raw and isinstance(raw[key], str):
                        thought = raw[key][:250]
                        parts.append(f"MY RECENT THOUGHTS:\n{thought}")
                        break

        # Semantic memories (related to the query)
        semantic = context.get("semantic_memories", [])
        if semantic:
            sem_text = "\n".join([
                f"- {m.get('content', m.get('description', ''))[:80]}"
                for m in semantic[:5]
            ])
            parts.append(f"RELATED MEMORIES:\n{sem_text}")

        # Memory summaries (historical context)
        summaries = context.get("memory_summaries", [])
        if summaries:
            sum_text = "\n".join([
                f"- {s.get('summary', '')[:100]}"
                for s in summaries[:3]
            ])
            parts.append(f"HISTORICAL CONTEXT:\n{sum_text}")

        return "\n\n".join(parts) if parts else "No context available."

    def _clean_for_voice(self, text: str) -> str:
        """Clean text for voice synthesis - remove formatting artifacts."""
        import re

        # Remove markdown formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.+?)`', r'\1', text)        # Code
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links

        # Remove emojis (basic pattern)
        text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)
        text = re.sub(r'[\U0001F300-\U0001F5FF]', '', text)
        text = re.sub(r'[\U0001F680-\U0001F6FF]', '', text)
        text = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', text)

        # Remove asterisks used for emphasis
        text = text.replace('*', '')

        # Collapse multiple spaces
        text = ' '.join(text.split())

        # Remove leading/trailing quotes if they wrap entire response
        text = text.strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]

        return text.strip()

    def _truncate_at_sentence(self, text: str, max_chars: int) -> str:
        """Truncate text at a sentence boundary."""
        if len(text) <= max_chars:
            return text

        truncated = text[:max_chars]

        # Try to find a sentence boundary
        for punct in ['. ', '! ', '? ']:
            last_sent = truncated.rfind(punct)
            if last_sent > max_chars // 2:
                return truncated[:last_sent + 1].strip()

        # Try period without space (end of text)
        if truncated.endswith('.'):
            return truncated

        last_period = truncated.rfind('.')
        if last_period > max_chars // 2:
            return truncated[:last_period + 1].strip()

        # No good boundary - just truncate with ellipsis
        return truncated.rstrip() + "..."

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about voice responses."""
        return {
            "response_count": self._response_count,
            "total_chars_spoken": self._total_chars_spoken,
            "avg_chars_per_response": (
                self._total_chars_spoken / self._response_count
                if self._response_count > 0 else 0
            ),
            "max_response_chars": self.max_response_chars,
            "has_client": self.client is not None,
            "model": self.model
        }

    def reset(self):
        """Reset statistics (called on system reset)."""
        self._response_count = 0
        self._total_chars_spoken = 0
        logger.info("VoiceResponder statistics reset")
