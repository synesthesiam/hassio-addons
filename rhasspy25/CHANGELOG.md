## [2.5.11] - 2021 Sep 10

### Added

- Option to allow "unknown" words to be recognized with Kaldi with Text FST grammar enabled
- Changeable "cancel" word that can be spoken at any time to trigger a recognition failure
- Preliminary support for Arabic (ar)
- Initial support for Vosk ASR (English, German, French, Spanish, Italian, Russian, Portuguese, Vietnamese, Arabic)
- New Larynx voices for German, Dutch, and English
- Multiple audio streams for Precise/Porcupine/Snowboy/Pocketsphinx wake word service (thanks Romkabouter)
- Raven speed optimizations for dynamic time warping code (thanks maxbachmann)
- Dialogue manager will convert audio files to WAV using soundfile and audioread
- dialogue.sound_suffixes profile setting controls file extensions searched for when dialogue feedback sound path is a directory
- rhasspy-speakers-cli-mqtt will convert audio bytes to WAV using soundfile and audioread
- Wake word systems can receive raw UDP audio from multiple sites, and forward it to MQTT (see wake.<system>.udp_site_info)

## Fixed

- Websocket queues are retained between restarts (thanks sabeechen)
- Avoid skipping 0 value in fsticuffs intent recognition
- Fix fsticuffs bug for dropping multiple words: [foo | bar]:

## Changed

- The rhasspy-silence CLI tool can now split audio by silence and trim silence

## [2.5.10] - 2020 Apr 10

### Added

- New version of Larynx with improved performance and 35 voices (20 English, 1 German, 3 French, 2 Spanish, 3 Dutch, 2 Italian, 1 Swedish, 3 Russian)
- Kaldi ASR model for Swedish (sv)
- Confidence and word timings for Kaldi ASR
- Minimum ASR confidence threshold for dialogue manager
- Detect AVX support and warn for Larynx, DeepSpeech, and Precise in Web UI
- Handle spaces in converter arguments with word!(converter, ...)
- rhasspy-tts-cli-hermes TTS commands may be Jinja2 templates (--use-jinja2)
- Support for MaryTTS effects (jasonhildebrand)
- customData added to hermes/nlu/query message
- customData is copied by NLU services from query to intent/intentNotRecognized
- lang property added for wake, speech_to_text, and intent profile sections
- Wake, ASR, NLU services all set lang properties if null
- Profile now has "parent" setting, allowing one profile to load settings from another
- Dialogue manager sound paths may be directories, from which a random WAV will be chosen each time (thanks plafue)

### Fixed

- Remote HTTP service sets site_id of satellite for ASR/NLU endpoints
- DeepSpeech token output (was letters, now words)
- Multiple values in custom converters are sent as a list on stdin
- Don't show restart/shutdown button if "sudo" isn't available (Docker, Hass.io)
- Added missing espeak phonemes for some profiles
- MaryTTS voice test in Web UI
- Remove dialogue session from site cache on end
- Don't throw error about system not configured if message is intent for satellite (schnopsi)
- Custom entities from /api/listen-for-command are passed through to NLU intent
- Slots inside sub-directories will properly show up in the web interface
- Use locks in dialogue manager to prevent multiple group satellite sessions during audio playback

### Changed

- /api/listen-for-command uses a proper wake workflow now (requires dialogue manager)
- Show absolute paths for custom models (precise, snowboy, porcupine) in Web UI
- TTS timeouts are computing using text length (dialogue.say_chars_per_second)

## [2.5.9] - 15 Jan 2021

### Added

- Add DeepSpeech v0.9 profiles for English, German, French, Spanish, Italian, and Polish (Jaco)
- Add streaming audio support for DeepSpeech (faster transcription)
- Settings for energy-based silence detection
- Max seconds for voice commands
- English voice for Larynx (kathleen)
- Reboot/shutdown menu in web UI
- Add text to speech testing tools in settings page
- Make it clearer in web UI when restarts are required
- _site_id meta slot to Home Assistant intents/events (bk90)

### Fixed

- Custom converters for fsticuffs and fuzzywuzzy
- fuzzywuzzy NluException: not enough values to unpack
- Download links for all profiles

### Changed

- Upgrade to Mozilla DeepSpeech v0.9
- Upgrade porcupine wake word system to 1.9
- Move OpenAPI page from /api/ to /openapi/
- Improved web UI for Raven keywords

## [2.5.8] - 2020 Nov 20

### Added

- Russian Kaldi profile and Larynx TTS voice
- Spanish Kaldi profile and Larynx TTS voice
- French Kaldi profile and Larynx TTS voice
- Italian Kaldi profile
- German Larynx TTS voice
- Volume scale (0-1) for feedback sounds and TTS
- rhasspy/asr/setVolume MQTT message and /api/setVolume HTTP endpoint
- rhasspy/asr/recordingFinished MQTT message sent immediately after silence detection
- Satellite site ids to intent handling settings in web UI
- Group separator for co-located satellites (dialogue.group_separator)
- num2words support for Swedish (Bostrom)

### Fixed

- Argument list for sound output command system (jrouly)
- Expand environment variables in TLS ca_certs
- spn silence phone in Swedish profile
- Use callback API in PyAudio to avoid buffer overrun
- HTTP API JSON should not be forced to ASCII

### Changed

- Default Kaldi language model type is now text FST instead of arpa

## [2.5.7] - 2020 Oct 15

### Added

- Add support for Czech language
- Add --http-root option to run web server with a different prefix

### Changed

- fuzzywuzzy examples database is deleted before training
- More graceful handling of missing site ids in dialogue manager

### Fixed

- Use session id instead of site id where possible in dialogue manager
- Fix silence phones in Vietnamese and profiles
- Model index bug in rhasspy-wake-snowboy-hermes

## [2.5.6] - 2020 Oct 3

### Added

- Multi-site support for dialogue manager
- Add "Text FST" language model type for Kaldi for strict grammar-based recognition
- UDP audio settings in web UI for Pocketsphinx wake word system
- Rudimentary SSML support in Google Wavenet TTS (digitalfiz)

### Changed

- JSON output from all services is no longer forced to be ASCII
- fuzzywuzzy performance improvement by using sqlite database (maxbachmann)
- Lots of documentation improvements (koen)
- Strip commans from replaced numbers ("one thousand, one hundred")
- Improve rhasspy-nlu performance (maxbachmann)
- Simplify Google Wavenet voice selection UI (Romkabouter)
- Fix local command when not using absolute path (DeadEnd)

## [2.5.5] - 2020 Jun 30

### Added

- Raven wake word system, based on Snips Personal Wakeword
- Support for Google WaveNet text to speech
- Support for OpenTTS/MozillaTTS
- Support for nanoTTS (fork of picoTTS)
- Energy-based silence detection in rhasspy-silence
- Preliminary support for SnipsNLU (not available yet in Docker)
- MQTT TLS in all services and web server
- More tutorials and documentation

### Changed

- Added train/restart confirmations back into web UI
- Fixed TTS language bug with eSpeak and picoTTS
- Use GNU autotools for source build (./configure, make, make install)
- Use pinned versions of profile files on GitHub

## [2.5.0] - 2020 Jun 05

First release of Rhasspy 2.5
