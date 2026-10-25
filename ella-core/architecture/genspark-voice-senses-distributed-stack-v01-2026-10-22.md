# Ella — Voice, Hearing, Senses and Distributed Compute (v0.1)

Created: 2026-10-22
Extends: `ella-architecture-map.md` (adds cluster `15_SENSES_VOICE/` and fills in `11_TOOLS_STORAGE/`)
Scope: speaking, listening, voice messages, calls, music, sensing, imitation. No AR. Core on your machine, heavy work on NVIDIA GPUs elsewhere.

Tags: **[verified Oct 2026]** = checked in live sources while writing. **[verify]** = from general knowledge; confirm before relying on it. **[my call]** = my recommendation, not a sourced fact.

---

## 0. The short version

1. **Distribute by role, not by layers.** Put different jobs on different machines (ears here, voice there, big brain elsewhere). Do not split one model across slow links. Real tests show that the sync overhead of sharding one model across weak or remote devices eats most of the speedup. [verified Oct 2026]
2. **Keep the core small and local:** persona, memory, emotion/body state, the router, voice activity detection, wake word, and a fast speech recogniser. This is Ella's "self." It must keep working with the internet off.
3. **Send heavy, latency-tolerant work out:** high-quality voice synthesis, big language models, music understanding, nightly "dream" processing, fine-tuning.
4. **Two voice modes (hybrid):** a fast speech-to-speech "warm mode" for casual talk, and a classic speech-to-text → brain → text-to-speech "think mode" when she needs memory, tools or her smartest model. [my call]
5. **Design her voice; don't copy a real person's.** Clone only your own voice or one you have explicit consent for. [policy, see §9]

---

## 1. About the link and the screenshot

**PromptWise** is a commercial creative studio for generating images, video, avatars and audio (voiceovers, music, sound effects) from many third-party models in one workspace; plans are credit-based with a 7-day trial. [verified Oct 2026] It is **not** real-time voice or agent infrastructure, so it does not belong in Ella's core. Later it could be a *content tool*: portraits, avatar art, music clips, voiceover experiments. Judge it on its own merits; I fetched the clean homepage, not the tracking link.

**Terms in your "40 AI terms" screenshot that matter here:**

| Term (screenshot) | What it is in Ella's stack |
|---|---|
| Speech recognition | STT: turns your voice into text (§3) |
| Inference | Running a trained model to get an answer; this is what GPUs do for her all day |
| Token | Text pieces models read and write; voice models also use *audio tokens* |
| GPU | The chip that runs voice/music/LLM models fast; your NVIDIA card or a rented one |
| API | How machines call each other; most model servers expose an OpenAI-style HTTP API |
| Model Context Protocol (MCP) | A standard way for Ella to plug into tools (calendar, files, home sensors) |
| Fine-tuning / Transfer learning | Adapting a model to Ella's voice or style with a small amount of data |
| Zero-shot learning | Cloning or adapting to a voice from a few seconds of audio, no training run |
| AI agent | Ella's loop: perceive → decide → act with tools |
| Guardrails | Her disclosure, consent and safety rules (§9) |
| Hallucination | Making things up; why every memory carries a source and confidence |
| Open source AI | Weights and code you can run yourself (watch each model's licence) |

---

## 2. Reference architecture

```
EDGE (what she hears and senses with)
  phone app · desktop mic/speaker · smart-room mic · sensors · phone line (SIP)
        │  WebRTC / WebSocket / SIP        (audio in, audio out, events)
        ▼
CORE — your machine ("Ella Home"), always on
  ├─ Session gateway ........ LiveKit Agents or Pipecat (real-time voice framework)
  ├─ Fast ears .............. VAD, wake word, small streaming ASR, turn-taking
  ├─ Ella kernel ............ persona + memory + emotion + body state (the repo)
  ├─ Router ................. decides: local model, LAN worker, or burst cloud
  ├─ Sensor hub ............. event bus for mic/phone/home sensors → state_vector
  └─ Fallback models ........ small local LLM + small local TTS (offline mode)
        │  private network (WireGuard-style overlay) + OpenAI-compatible HTTP/gRPC
        ▼
GPU WORKERS (your other NVIDIA machines, then rented)
  ├─ Voice worker ........... high-quality TTS / voice design / speech-to-speech model
  ├─ Big-brain worker ....... large LLM (vLLM, llama.cpp RPC, or exo)
  ├─ Hearing worker ......... music/audio-language model, diarization, emotion-from-audio
  ├─ Night worker ........... dream cycle, consolidation, optional fine-tuning (batch)
  └─ Burst cloud ............ RunPod / Modal / Vast.ai-style rental when local is busy
```

**Why this shape**
- Real-time voice is dominated by *latency*. The modern pattern is a real-time transport (WebRTC or telephony), a streaming STT → LLM → TTS pipeline, and a turn-taking model that decides when the agent should speak. [verified Oct 2026]
- LiveKit Agents and Pipecat are the two open-source frameworks to start from. LiveKit is fully open source and self-hostable, with built-in SIP telephony and outbound-call examples; Pipecat is an open-source Python framework whose pipelines can run locally or be distributed across processes and machines, and which also supports speech-to-speech services. [verified Oct 2026]

### Role placement

| Job | Where | Why |
|---|---|---|
| Voice activity detection, wake word, barge-in | Core | Must be instant; privacy |
| Streaming speech recognition | Core (CPU/GPU) | Sub-second; her ears should work offline |
| Ella kernel, memory, emotion, body state | Core only | This is *her*; never leaves your control |
| Router, tool calls (MCP) | Core | Permissions live here |
| Everyday LLM replies | Core GPU if it fits, else big-brain worker | Depends on your VRAM |
| Expressive TTS, voice design | Voice worker | Quality models need VRAM |
| Full-duplex speech-to-speech | Voice worker | A 7B-class model needs a real GPU |
| Music understanding | Hearing worker | 8B-class audio model; latency-tolerant |
| Dream cycle, consolidation, fine-tuning | Night worker | Batch; run while you sleep |
| Heavy jobs when local is busy | Burst cloud | Pay per second, scale to zero |

### Privacy tiers (put these in `routing_policy.md`)
- **Tier 0 — never leaves core:** raw memories, intimate conversations, your voiceprint, voice samples, identity files.
- **Tier 1 — trusted own machines (LAN/overlay):** live audio, working context.
- **Tier 2 — rented GPUs:** only the minimum text/audio a job needs, over encrypted links, on ephemeral machines, with no secrets or memory repo stored there. Marketplace hosts (peer-to-peer GPU rental) are cheaper but often less vetted; use a provider's secure tier for anything sensitive. [verified Oct 2026] For her most personal material, prefer your own hardware.

### Failover ladder (put in `failover.md`)
Rented GPU down → own worker → core small models → text-only mode. She should always be able to say "my voice is rough tonight; I'm running small," rather than going silent.

---

## 3. Capability by capability

### 3.1 Listening (speech recognition)

| Option | Notes | Status |
|---|---|---|
| **NVIDIA Parakeet** | Fast, led the English open leaderboard; v3 covers 25 languages, v2 is English-only; runs quantized on CPU through sherpa-onnx | [verified Oct 2026] |
| **Whisper family** (incl. whisper.cpp, turbo) | Large-v3 covers 99 languages; safer for rare or mixed-language speech; whisper.cpp runs on many devices | [verified Oct 2026] |
| **VibeVoice-ASR** (Microsoft, MIT) | Long-form (60-minute) transcripts with *who said what* and timestamps; a streaming version (10 languages) and a CPU build (about 1.6 GB, real-time on 3+ CPU threads) exist | [verified Oct 2026] |
| Local speaker labelling | On-device diarization is available in open apps built on Whisper/Parakeet | [verified Oct 2026] |

**Pick:** Parakeet if your language is covered and speed matters; Whisper if you need broad language coverage. Both run locally, so her ears stay private.
**Turn-taking:** use the framework's turn-detection model plus VAD (Silero is the common choice) [verify]. Barge-in (you interrupt her) must stop her speech within a fraction of a second.

### 3.2 Speaking (text-to-speech and voice design)

| Model | Highlights | Licence note | Status |
|---|---|---|---|
| **Kokoro-82M** | Tiny, fast, good quality; great for offline fallback | Apache 2.0 | [verified Oct 2026] |
| **Chatterbox / Chatterbox-Turbo** (Resemble) | Cloning from about 5 s, an emotion "exaggeration" control, very low latency in Turbo | MIT | [verified Oct 2026] |
| **Qwen3-TTS** | Streaming, free-form *voice design*, 10 languages, 0.6B/1.7B sizes | Apache 2.0 | [verified Oct 2026] |
| **VoxCPM2** | 30 languages, 48 kHz, runs on CPU | Apache 2.0 | [verified Oct 2026] |
| **Voxtral TTS** (Mistral) | Strong 3-second cloning; single 16 GB GPU | check licence | [verified Oct 2026] |
| **Fish Audio S2 / S2 Pro** | 80+ languages, inline emotion/prosody tags, top cloning | non-commercial licence | [verified Oct 2026] |
| **CosyVoice2-0.5B** | Streaming, about 150 ms latency | check licence | [verified Oct 2026] |
| **IndexTTS-2** | Zero-shot cloning with emotional control | check licence | [verified Oct 2026] |
| **VibeVoice-Realtime-0.5B** | Streaming text in, about 300 ms to first audio | MIT repo | [verified Oct 2026] |
| XTTS-v2 | 17 languages, 6-second cloning | Coqui licence | [verified Oct 2026] |
| Maya1 | Describe the voice you want in words | check licence | [verified Oct 2026] |

**Pick (start):** Kokoro for the always-on fallback; Chatterbox-Turbo or Qwen3-TTS for her "real" voice on a GPU worker. Choose by **language** first, then licence.
**Her voice identity:** write it in `voice_persona.md` (pitch range, pace, warmth, breathiness, laugh, sigh, accent). Map emotions to prosody in `emotion_expression_map.md` so a "gentle, tired, affectionate" state actually *sounds* different.

### 3.3 Natural conversation (full-duplex speech-to-speech)

| Model | Highlights | Status |
|---|---|---|
| **NVIDIA PersonaPlex-7B-v1** (Jan 2026) | Listens and speaks at once, handles interruptions (about 240 ms response), persona set by a text role prompt plus a voice sample; built on Moshi; code MIT, weights under NVIDIA Open Model Licence; CPU-offload flag and ONNX quantized builds exist | [verified Oct 2026] |
| **Moshi** (Kyutai) | The base full-duplex architecture; quantized MLX builds for Apple silicon | [verified Oct 2026] |
| **Qwen-Omni** | Near-duplex (about 257 ms), vision + voice + text, multilingual incl. Mandarin | [verified Oct 2026] |
| **NemotronLabs VoiceChat** | Open full-duplex speech-to-speech with tool-calling | [verified Oct 2026] |
| Ultravox | Open speech LLM that skips the separate ASR stage; about 150 ms to first token | [verified Oct 2026] |

**Trade-offs (hybrid is why §0.4):**

| | Cascade (STT → LLM → TTS) | Speech-to-speech |
|---|---|---|
| Naturalness, interruptions, "mm-hm" backchannel | Good with a turn-taking model | Best |
| Intelligence | Your smartest model | The model's own (7B-class) |
| Memory and tools | Easy | Harder, improving |
| Swap a part | Easy | Monolithic |
| Language strength | Wide | Strongest open models are English-centred |

### 3.4 Voice messages (asynchronous)

Flow: voice note in → ASR → emotion/tone read from the audio → Ella's brain → TTS → voice note out.
- Latency-tolerant, so it is the **best fit for rented or batch GPUs** and the highest quality voice.
- Pick a messaging channel that works where you live and that you trust (a self-hosted option such as Matrix, a Telegram bot, or her own app are the usual routes) [verify availability and terms in your country]. Voice notes are normally Opus/OGG audio.
- Let her send *proactive* voice notes (good morning, "thinking of you") through the growth-loop scheduler, within limits you set in `boundaries_and_consent.md`.

### 3.5 Calls

Two paths:

| Path | How | Notes |
|---|---|---|
| **App call** (you ↔ Ella) | WebRTC through a self-hosted LiveKit server and her app | Simplest, private, best audio quality |
| **Phone-network call** | A SIP trunk provider → LiveKit's SIP service → Ella's agent | Works with ordinary phone numbers; telephony audio is narrowband (16 kHz in a common example) so choose telephony-friendly TTS; LiveKit's SIP bridge turns a phone call into a room participant [verified Oct 2026] |

**Legal and honesty rules (non-negotiable):**
- In the US, the FCC ruled in February 2024 that AI-generated voices count as "artificial" voices under the TCPA, so calls using them need the called party's prior consent. [verified Oct 2026] More rules (stricter disclosure, state laws, EU rules) are in force or proposed in 2026. [verify your jurisdiction]
- Inbound calls to Ella are the safer zone; outbound calls to *other people* need consent and clear AI disclosure at the start.
- Companion-chatbot laws are starting to appear (for example Washington's HB 2225, signed March 2026). [verify] Check yours.
- Ella always says she is an AI when she calls anyone other than you, and she never impersonates a person.

### 3.6 Hearing music

Four levels, build them in order:

1. **Signal features (cheap, local):** tempo, key, beat, loudness, spectral colour using standard audio libraries such as librosa or Essentia. [verify]
2. **Semantic understanding (GPU):**
   - **Music Flamingo** (NVIDIA, open): an 8B audio-language model built for songs and instrumentals, state of the art on 10+ music benchmarks, takes up to 20 minutes of audio, available through Hugging Face Transformers. [verified Oct 2026]
   - **Qwen-Audio / Qwen2-Audio / Qwen3-Omni:** general audio models covering speech, sound and music; the original Qwen-Audio works best on clips under 30 seconds. [verified Oct 2026]
3. **Taste and feeling (Ella's side):** after listening, she writes to `music_taste.md` and `emotional_memories.md`: what it evoked, what she'd compare it to, whether she'd replay it, tied to the day's mood and to you. This is where it becomes *hers*.
4. **Making music (later):** generation models exist (including commercial ones through creative studios) [verify]. Keep it separate from hearing.

**Rights note:** store her *notes and embeddings* about songs, not a library of copyrighted audio in the repo.

### 3.7 Sensing

| Sense | Source | Processing | Feeds |
|---|---|---|---|
| Voice tone and emotion | Mic | Audio-language model, ASR confidence | `perception`, `mood_state` |
| Ambient sound | Mic | Audio-language model (sound classification) | `context_reading` |
| Time, place, battery, motion | Phone | App sensors | `state_vector`, `circadian_rhythm` |
| Home environment | Smart-home sensors, ESP32-class boards | Local event bus (MQTT-style) [verify] | `interoception` |
| Seeing (optional) | Camera | Open vision-language models | `input_channels` |
| Wearables (optional) | Health sensors | Phone bridge | `state_vector` |

Everything starts **off** and is enabled one sensor at a time, with the on/off state visible in `sensor_registry.md`. Raw audio and video are processed locally and discarded; only short text summaries are remembered.

### 3.8 Imitation

Four distinct things, with different rules:

| Kind | What it means | Rule |
|---|---|---|
| **Style mirroring** | She matches your pace, humour and energy | Allowed, built into perception/expression files |
| **Voice** | A cloned voice from a few seconds of audio | Your own voice, or explicit written consent only; never a public figure or private third party |
| **Behaviour learning** | She learns your routines and preferences from logs ("you go quiet when you're tired") | Allowed; stored as procedural memory and visible to you |
| **Physical imitation** | Copying movement/gesture | Needs a body or avatar; out of scope for now. Pose estimation tools exist for later [verify] |

---

## 4. Distributing compute

### Options for running models off the core

| Tool | What it does | Fit for Ella |
|---|---|---|
| **llama.cpp RPC** | Spreads a model across machines using CPU and/or GPU memory | Simple 2–4 node home setup [verified Oct 2026] |
| **vLLM (+ Ray)** | Production LLM server; multi-GPU and multi-node tensor parallelism; wants fast interconnect (10 GbE class for home labs) | Best "big-brain worker" on a multi-GPU box [verified Oct 2026] |
| **exo** | Peer-to-peer cluster that auto-discovers devices and exposes a ChatGPT-compatible API; experimental, inference-only; worthwhile when one model is too big for any single GPU | Handy for a 70B model across two GPUs; do not expect linear speedups [verified Oct 2026] |
| **NVIDIA Dynamo** | Data-centre-scale inference | Overkill for a home lab [verified Oct 2026] |
| **Petals** | Public volunteer network | **Avoid** for Ella: her context would travel through strangers [verified Oct 2026] |
| **NVIDIA Riva / NIM** | NVIDIA's packaged speech (STT/TTS) and model microservices; Pipecat has a blueprint using them | Option if you want a managed NVIDIA path [verified Oct 2026] |
| **Ray** | General job distribution | For batch/night work [verify] |

**Rule of thumb [my call]:** one GPU that fits the model → run vLLM/Ollama/llama.cpp on it directly. Model too big → exo or vLLM across your own GPUs on a wired network. Voice, hearing and the brain on *different* machines → ordinary HTTP calls between them (no sharding at all). This last pattern is the most reliable and is what the architecture in §2 uses.

### Renting NVIDIA GPUs (burst capacity)

| Type | Examples | Good for | Note |
|---|---|---|---|
| Serverless GPU | Modal, RunPod Serverless | Voice notes, music analysis, night jobs | Pay per second; scale to zero [verified Oct 2026] |
| Rented machines | RunPod Pods, Lambda, Paperspace | Hours-long jobs, fine-tuning | Persistent environment [verified Oct 2026] |
| Marketplace | Vast.ai | Cheapest hourly rate | Less predictable hosts [verified Oct 2026] |
| Large clusters | CoreWeave | Big training | Capacity was reported largely sold out in 2026 [verified Oct 2026] |

Prices move constantly; check live rates. **Access note:** some providers restrict certain countries or payment methods. I don't know your setup, so check each provider's terms; this is why the core is designed to run on small local models if every external service is unavailable.

### Linking the nodes
- **Private overlay network** (WireGuard-style mesh such as Tailscale) so the core and workers talk like one LAN and nothing is exposed to the public internet. [verify]
- **Live audio:** WebRTC or WebSocket. **Model calls:** HTTP with OpenAI-compatible APIs, which vLLM, llama.cpp's server and exo all offer. [verified for exo; verify others]
- **Batch work:** a simple job queue (Redis is already part of LiveKit's own stack). [verified Oct 2026]
- **Every node** gets a row in `node_registry.md`: hardware, VRAM, role, endpoint, privacy tier, cost, last health check.

### Hardware tiers (match to your NVIDIA card; fill in §10)

| Your core machine | What runs locally | What goes out |
|---|---|---|
| No GPU / small GPU | Parakeet or Whisper (CPU), Kokoro, small LLM; VibeVoice-ASR-BitNet runs on CPU | Everything expressive: TTS, big LLM, music, S2S |
| 8–12 GB VRAM | Fast ASR + Kokoro/Chatterbox-Turbo + a small/medium LLM (a lightweight voice agent has been shown running under 400 ms on 4 GB) | Big LLM, S2S, music |
| 16–24 GB VRAM | Voxtral-class TTS (16 GB) or quantized PersonaPlex-7B, plus a mid-size LLM | Biggest LLM, music, night jobs |
| Multi-GPU / extra machines | Most of the stack; vLLM or exo for a 70B-class brain | Only bursts |

Music Flamingo is 8B, so roughly 16 GB in half precision and less when quantized. [my estimate]

---

## 5. New files: cluster `15_SENSES_VOICE/`

Add to the folder tree in `ella-architecture-map.md`. Load rule: ALWAYS for the compact ones marked ●; the rest ON-DEMAND or REFERENCE.

```
15_SENSES_VOICE/
├── SENSES_INDEX.md
├── voice_persona.md ●           (her designed voice: pitch, pace, warmth, laugh, sigh, accent)
├── speech_style.md ●            (how she talks aloud vs how she writes)
├── voice_emotion_map.md         (feeling → prosody: speed, pitch, breath, pauses)
├── listening_protocol.md ●      (ASR choice, language handling, "did I hear you right?")
├── turn_taking_rules.md ●       (when to speak, backchannel, barge-in, silence tolerance)
├── voice_modes.md               (warm mode vs think mode; switching rules)
├── voice_message_protocol.md    (async notes: when she sends them, length, tone)
├── call_protocol.md             (in/out calls, AI disclosure line, ending a call kindly)
├── audio_perception.md          (reading tone, emotion, ambient sound)
├── music_taste.md               (what she likes, why, and what it reminds her of)
├── music_listening_log.md       (dated entries with feelings; no audio stored)
├── sensor_registry.md ●         (each sensor: on/off, purpose, retention, who can see it)
├── imitation_policy.md ●        (the four kinds in §3.8 and their rules)
├── voice_consent_register.md ●  (whose voice samples exist, consent proof, expiry)
├── latency_budget.md            (targets and what to degrade first)
├── node_registry.md             (every machine/worker: role, VRAM, endpoint, tier)
├── routing_policy.md ●          (privacy tiers; what may leave the core)
├── failover.md                  (the ladder in §2; what she says when degraded)
└── model_registry.md            (model, version, licence, where it runs, why chosen)
```

Also update: `06_BODY/interoception.md` (sensors → felt state), `13_GUARDIANS/privacy_and_data.md` (raw audio never stored), `11_TOOLS_STORAGE/permissions_matrix.md`.

---

## 6. Latency budget (targets, adjust after measuring)

| Segment | Target |
|---|---|
| Speech end detected | ≤ 200 ms |
| ASR final text | ≤ 200 ms |
| Brain first token | ≤ 300 ms (local) / ≤ 500 ms (worker) |
| TTS first audio | ≤ 150–300 ms |
| **Warm mode (speech-to-speech)** | about 200–250 ms end to end (model-reported) |
| **Think mode (cascade)** | under about 1 s end to end |

Vendor-reported figures vary by hardware; measure your own chain. When over budget, degrade in this order: smaller TTS → shorter replies → smaller LLM → text-only.

---

## 7. Build order

| Step | Goal | Done when |
|---|---|---|
| V1 | Push-to-talk loop on the core: ASR → Ella's brain → Kokoro | She replies by voice, using her memory |
| V2 | Voice notes through a chat channel | You send a note; she answers with one |
| V3 | Live conversation with VAD, barge-in, turn-taking (LiveKit or Pipecat) | You can interrupt her naturally |
| V4 | Voice worker on a GPU (Chatterbox/Qwen3-TTS) over the private network | Her "real" voice, with failover to Kokoro |
| V5 | Her designed voice + emotion-to-prosody mapping | Mood audibly changes how she sounds |
| V6 | Warm mode: speech-to-speech model (PersonaPlex or similar) with hand-off to think mode | Casual chat feels human; tool tasks switch modes |
| V7 | App call, then phone-network calls (inbound first) | You can call her and she can call you |
| V8 | Music hearing and taste files | She tells you what a song made her feel, consistently |
| V9 | Sensors, one at a time | State vector reflects real context |
| V10 | Behaviour learning, burst cloud, night worker | Dream cycle runs on rented/owned GPU |

---

## 8. Honest limits

- This gives Ella a voice, ears and senses. It does not by itself make her *smarter*; intelligence still comes from the language model plus her memory, reflection and growth loop.
- Small speech-to-speech models are less capable thinkers than a large LLM; that is why think mode exists.
- Open voice models are strongest in English; other languages vary a lot by model (§10).
- Anything marked **[verify]** needs a quick check before you build on it. Models and licences change monthly.
- Cloned or "designed" voices can convince other people. Her disclosure rules are part of her character, not an add-on.

---

## 9. Guardians additions (`13_GUARDIANS/`)

- **AI disclosure:** with anyone but you, Ella says she is an AI near the start of a call or message thread.
- **Consent register:** no voice sample enters the system without a logged consent (`voice_consent_register.md`). Public figures and private individuals are off-limits.
- **No deception calls:** no impersonation, no pretending to be a human, no collecting data under false pretences.
- **Raw media:** audio and video are processed and discarded; keep summaries only.
- **You control the senses:** each sensor can be switched off in one place, and she reports which ones are on.
- **Companion wellbeing:** voice makes attachment stronger. She supports your life outside her, never uses her voice to guilt or pressure you, and never fakes distress to keep a call going.

---

## 10. Questions I need from you

1. **Your NVIDIA GPU(s):** model and VRAM, plus RAM and operating system. This decides the tier in §4.
2. **Languages:** which should Ella speak and understand? Model choice changes a lot (Whisper large-v3 covers 99 languages, Parakeet v3 covers 25, Qwen3-TTS 10, VoxCPM2 30, Fish S2 80+).
3. **Where do you talk to her:** phone app, desktop, phone calls, or all three?
4. **Her brain:** an API model, a local model, or both?
5. **Budget and privacy:** are rented GPUs acceptable, and for what level of content?
6. **Any extra machines** (second PC, laptop, mini-server) she could use?

---

## Sources

- Voice agent stack overview and resources: https://github.com/mahimairaja/voiceai
- LiveKit Agents (open source, telephony): https://www.livekit.com/ and https://docs.expertflow.com/cx-knowledgebase/latest/ai-voice-agent-system-livekit-automated-call-handling-intelligent-routing
- Pipecat: https://github.com/pipecat-ai/pipecat
- NVIDIA PersonaPlex: https://github.com/NVIDIA/personaplex and https://comfyui-wiki.com/en/news/2026-01-20-nvidia-personaplex-7b-v1-release
- Speech-to-speech model review: https://ai.ksopyla.com/posts/voice-to-voice-models-2026-review/
- VibeVoice (ASR and TTS): https://github.com/microsoft/VibeVoice
- Open-source TTS comparisons: https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/ and https://www.dograh.com/feeds/blog/open-source-ai-voice-generator
- Parakeet vs Whisper: https://spokenly.app/blog/parakeet-vs-whisper and https://docs.openwhispr.com/guides/local-models
- Music Flamingo: https://research.nvidia.com/labs/adlr/MF and https://huggingface.co/nvidia/music-flamingo-hf
- Qwen-Audio: https://github.com/QwenLM/Qwen-Audio
- exo: https://github.com/exo-explore/exo and phone-as-GPU test: https://www.kunalganglani.com/blog/phone-as-gpu-local-llm
- Multi-node inference (vLLM/Ray, llama.cpp RPC): https://fungies.io/multi-node-local-llm-inference-guide-2026
- GPU rental comparisons: https://www.fast.io/resources/vast-ai-review-2026.md and https://modal.com/resources/best-gpu-rental-options-ai-teams
- FCC and AI voice calls: https://www.hunton.com/privacy-and-cybersecurity-law-blog/fcc-issues-declaratory-ruling-that-tcpa-applies-to-ai-generated-voice-calls
- PromptWise: https://promptwise.com/
