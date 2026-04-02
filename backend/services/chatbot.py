"""
IntervYou AI Coach — Ollama LLM Service
Local LLM-powered interview coaching chatbot
"""
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class InterviewCoach:
    """AI interview coach powered by local Ollama LLM"""

    _model = None
    _chat_template = None
    _feedback_template = None
    _analysis_template = None

    @classmethod
    def _initialize(cls):
        if cls._model is not None:
            return
        try:
            cls._model = OllamaLLM(model="qwen3:1.7b")

            cls._chat_template = ChatPromptTemplate.from_template("""/no_think
You are IntervYou AI Coach. Give concise interview advice.

Context: {context}
Question: {question}

Reply in 2-3 short paragraphs. Be practical and encouraging.
""")

            cls._feedback_template = ChatPromptTemplate.from_template("""
You are IntervYou AI Coach. A candidate just completed an interview practice session. Provide a personalised coaching summary.

Session data:
- Job role: {job_role}
- Difficulty level: {level}
- Overall score: {overall_score}/100
- Number of questions answered: {num_questions}

Per-question results:
{question_results}

Provide:
1. A brief overall assessment (2 sentences)
2. Top 2 strengths observed
3. Top 2 areas for improvement with specific tips
4. One motivational closing sentence

Keep it concise and actionable.

Answer:
""")

            cls._analysis_template = ChatPromptTemplate.from_template("""/no_think
Analyse this interview answer briefly.

Question: "{question}"
Answer: "{transcript}"
Score: {overall_score}/100 | Relevance: {relevance_pct}% | Fluency: {fluency_pct}% | Rate: {speaking_rate} wpm | Fillers: {filler_count} | Pauses: {pause_count} | Mode: {input_mode}

Reply in this exact format (keep each section to 1-2 sentences):

CONFIDENCE: [Low/Moderate/High] — [why]
CONTENT: [quality assessment]
DELIVERY: [pace and filler assessment]
3 TIPS: 1) [tip] 2) [tip] 3) [tip]
BETTER ANSWER: [suggested improvement]
""")

            print('Ollama LLM initialized with qwen3:1.7b model')
        except Exception as e:
            print(f'Failed to initialize Ollama LLM: {e}')
            print('Make sure Ollama is running: ollama serve')
            print('And qwen3:1.7b is installed: ollama pull qwen3:1.7b')
            raise

    @classmethod
    def chat(cls, question: str, context: str = '') -> str:
        """Generate a coaching response to a user message."""
        cls._initialize()
        try:
            chain = cls._chat_template | cls._model
            return chain.invoke({'context': context, 'question': question})
        except Exception as e:
            print(f'Ollama chat error: {e}')
            return (
                'I apologise, but I am having trouble connecting to the AI model right now. '
                'This might be because the Ollama service is not running. '
                'Please make sure Ollama is started (run: ollama serve) and try again.'
            )

    @classmethod
    def generate_session_feedback(cls, job_role: str, level: str,
                                  overall_score: float, question_results: list) -> str:
        """Generate personalised feedback for a completed session."""
        cls._initialize()
        try:
            results_text = ''
            for i, r in enumerate(question_results, 1):
                results_text += (
                    f'Q{i}: "{r.get("question", "")}" — '
                    f'Score: {r.get("overall_score", 0)}, '
                    f'Relevance: {r.get("relevance_score", 0)}, '
                    f'Fluency: {r.get("fluency_score", 0)}\n'
                    f'   Transcript: {(r.get("transcript", "") or "")[:150]}\n'
                )

            chain = cls._feedback_template | cls._model
            return chain.invoke({
                'job_role': job_role,
                'level': level,
                'overall_score': overall_score,
                'num_questions': len(question_results),
                'question_results': results_text
            })
        except Exception as e:
            print(f'Ollama session feedback error: {e}')
            return ''

    @classmethod
    def analyze_response(cls, question: str, transcript: str, metrics: dict,
                         input_mode: str = 'voice') -> str:
        """Generate deep LLM-powered analytical feedback for a single answer."""
        cls._initialize()
        try:
            chain = cls._analysis_template | cls._model
            return chain.invoke({
                'question': question,
                'transcript': transcript or '(No speech detected)',
                'input_mode': input_mode,
                'overall_score': metrics.get('overall_score', 0),
                'relevance_pct': round(metrics.get('relevance_score', 0) * 100),
                'fluency_pct': round(metrics.get('fluency_score', 0) * 100),
                'speaking_rate': metrics.get('speaking_rate', 0),
                'filler_count': metrics.get('filler_count', 0),
                'pause_count': metrics.get('pause_count', 0)
            })
        except Exception as e:
            print(f'Ollama analysis error: {e}')
            return ''

    @classmethod
    def build_context(cls, history: list) -> str:
        """Build context string from conversation history (last 10 messages)."""
        if not history:
            return ''
        recent = history[-10:]
        parts = []
        for msg in recent:
            role = 'User' if msg.get('role') == 'user' else 'Coach'
            parts.append(f'{role}: {msg.get("content", "")}')
        return '\n'.join(parts)
