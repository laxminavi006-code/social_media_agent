# agent.py
import os
import base64
from groq import Groq
from config import GROQ_API_KEY, MODEL_FALLBACKS

class SocialMediaAgent:
    def __init__(self, api_key=None, models=None):
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise Exception("GROQ_API_KEY not set. Put it in .env or config.py")
        self.client = Groq(api_key=self.api_key)
        self.models = models or MODEL_FALLBACKS

    def _try_models(self, prompt, temperature=0.7, max_tokens=300, image_data_url=None):
        last_error = None
        for model in self.models:
            try:
                messages = [
                    {"role": "system", "content": "You are a creative social media assistant that writes captions, hashtags, reels scripts, and social media plans."},
                    {"role": "user", "content": prompt}
                ]
                # If image provided, append its data URL in the prompt (best-effort)
                if image_data_url:
                    messages.append({"role": "user", "content": f"[IMAGE_DATA]{image_data_url}"})

                resp = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                text = resp.choices[0].message.content
                return {"model": model, "text": text}
            except Exception as e:
                last_error = e
                # try next model
                continue
        # if all failed, raise last error
        raise last_error or Exception("No available models")

    def generate_advanced_captions(self, topic, creativity=0.7):
        prompt = f"""
Generate 5 distinct social-media captions for: "{topic}".
Label each caption:
CINEMATIC:
GEN-Z:
LUXURY:
VIRAL-SEO:
STORYTELLING:
Return only labeled captions.
"""
        return self._try_models(prompt, temperature=creativity, max_tokens=400)

    def generate_reel_script(self, topic, creativity=0.7):
        prompt = f"""
Create a tight 15-20 second Instagram Reels script for: "{topic}".
Return labeled sections exactly: HOOK:, VISUALS:, VOICEOVER:, CTA:
"""
        return self._try_models(prompt, temperature=creativity, max_tokens=260)

    def generate_hashtags(self, topic, count=20):
        prompt = f"""
Generate {count} high-quality hashtags for: "{topic}".
Group them as: HIGH_REACH:, MEDIUM_REACH:, LOW_COMPETITION:
Return exactly in that format.
"""
        return self._try_models(prompt, temperature=0.45, max_tokens=260)

    def generate_weekly_plan(self, topic, timezone="Asia/Kolkata"):
        prompt = f"""
Create a 7-day content plan for: "{topic}".
For Day 1..Day 7, include:
- POST TYPE:
- SUGGESTED TIME: (e.g. 6:30 PM {timezone})
- CAPTION: (1-2 lines)
- HASHTAGS: (5-10)
Return a numbered list.
"""
        return self._try_models(prompt, temperature=0.7, max_tokens=700)

    def score_caption(self, caption, topic="general"):
        prompt = f"""
You are a social media strategist. Score the following caption for topic '{topic}'.
Caption:
\"\"\"{caption}\"\"\"

Return:
SCORE: <0-100>
RATIONALE:
- ...
IMPROVEMENT: <one-line>
"""
        return self._try_models(prompt, temperature=0.25, max_tokens=220)

    def image_to_caption(self, image_bytes, topic_hint=None):
        # Convert image bytes to base64 data URL (jpeg) — keep small but works
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{b64}"
        prompt = "Write an Instagram caption for the image. Keep it short and engaging."
        if topic_hint:
            prompt += f" Topic hint: {topic_hint}"
        return self._try_models(prompt, temperature=0.7, max_tokens=220, image_data_url=data_url)
