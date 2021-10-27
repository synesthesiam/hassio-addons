# OpenTTS (el)

Unifies access to multiple open source text to speech systems and voices for many languages.

Supports a [subset of SSML](#ssml) that can use multiple voices and text to speech systems!

[Listen to voice samples](https://synesthesiam.github.io/opentts/)

[View source code](https://github.com/synesthesiam/opentts)

## Settings

* `cache_dir`
    * Directory to cache generated WAV files
    * Leave empty to disable (default, HA already has a TTS cache)
* `debug`
    * If true, DEBUG messages are printed to the log
    * Default is false
* `larynx_quality`
    * Default quality setting for the [Larynx TTS](https://github.com/rhasspy/larynx) system
    * Default is "high", choices are "high", "medium", "low" (use "low" for Raspberry Pi)
* `larynx_denoiser_strength`
    * Amount to apply denoiser during [Larynx TTS](https://github.com/rhasspy/larynx) post-processing
    * Default is 0.005 (higher value reduces noise, but distorts voice)
* `larynx_noise_scale`
    * Volatility of [Larynx TTS](https://github.com/rhasspy/larynx) vocalization
    * Default is 0.667, range is 0-1. Higher values make the voice less monotone
* `larynx_length_scale`
    * Speed of [Larynx TTS](https://github.com/rhasspy/larynx) speech
    * Default is 1.0, lower values are faster, higher values are slower

## MaryTTS Compatible Endpoint

Use OpenTTS as a drop-in replacement for [MaryTTS](https://www.home-assistant.io/integrations/marytts/).

Add to your `configuration.yaml` file:

```yaml
tts:
  - platform: marytts
    port: 5500
    voice:larynx:harvard
```

The `voice` format is `<TTS_SYSTEM>:<VOICE_NAME>`. Visit the OpenTTS web UI and copy/paste the "voice id" of your favorite voice here.

You may leave out the `port` setting if you configure the OpenTTS host port to be 59125 instead of 5500.

If your input text begins with a left angle bracket (`<`), it will be interpreted as [SSML](#ssml).

## SSML

A subset of [SSML](https://www.w3.org/TR/speech-synthesis11/) is supported:

* `<speak>` - wrap around SSML text
    * `lang` - set language for document
* `<s>` - sentence (disables automatic sentence breaking)
    * `lang` - set language for sentence
* `<w>` / `<token>` - word (disables automatic tokenization)
* `<voice name="...">` - set voice of inner text
    * `voice` - name or language of voice
        * Name format is `tts:voice` (e.g., "glow-speak:en-us_mary_ann") or `tts:voice#speaker_id` (e.g., "coqui-tts:en_vctk#p228")
        * If one of the supported languages, a preferred voice is used (override with `--preferred-voice <lang> <voice>`)
* `<say-as interpret-as="">` - force interpretation of inner text
    * `interpret-as` one of "spell-out", "date", "number", "time", or "currency"
    * `format` - way to format text depending on `interpret-as`
        * number - one of "cardinal", "ordinal", "digits", "year"
        * date - string with "d" (cardinal day), "o" (ordinal day), "m" (month), or "y" (year)
* `<break time="">` - Pause for given amount of time
    * time - seconds ("123s") or milliseconds ("123ms")
* `<sub alias="">` - substitute `alias` for inner text

## Supported Text to Speech Systems

Below is a list of the supported TTS systems and voice counts by language.

* [Larynx](https://github.com/rhasspy/larynx-runtime)
    * English (27), German (7), French (3), Spanish (2), Dutch (4), Russian (3), Swedish (1), Italian (2), Swahili (1)
    * Model types available: [GlowTTS](https://github.com/rhasspy/glow-tts-train)
    * Vocoders available: [HiFi-Gan](https://github.com/rhasspy/hifi-gan-train) (3 levels of quality)
    * Patched embedded version of Larynx 1.0
* [Glow-Speak](https://github.com/rhasspy/glow-speak)
    * English (2), German (1), French (1), Spanish (1), Dutch (1), Russian (1), Swedish (1), Italian (1), Swahili (1), Greek (1), Finnish (1), Hungarian (1), Korean (1)
    * Model types available: [GlowTTS](https://github.com/rhasspy/glow-tts-train)
    * Vocoders available: [HiFi-Gan](https://github.com/rhasspy/hifi-gan-train) (3 levels of quality)
* [Coqui-TTS](https://github.com/coqui-ai/TTS)
    * English (110), Japanese (1), Chinese (1)
    * Patched embedded version of Coqui-TTS 0.3.1
* [nanoTTS](https://github.com/gmn/nanotts)
    * English (2), German (1), French (1), Italian (1), Spanish (1)
* [MaryTTS](http://mary.dfki.de)
    * English (7), German (3), French (4), Italian (1), Russian (1), Swedish (1), Telugu (1), Turkish (1)
    * Includes [embedded MaryTTS](https://github.com/synesthesiam/marytts-txt2wav)
* [flite](http://www.festvox.org/flite)
    * English (19), Hindi (1), Bengali (1), Gujarati (3), Kannada (1), Marathi (2), Punjabi (1), Tamil (1), Telugu (3)
* [Festival](http://www.cstr.ed.ac.uk/projects/festival/)
    * English (9), Spanish (1), Catalan (1), Czech (4), Russian (1), Finnish (2), Marathi (1), Telugu (1), Hindi (1), Italian (2), Arabic (2)
    * Spanish/Catalan/Finnish use [ISO-8859-15 encoding](https://en.wikipedia.org/wiki/ISO/IEC_8859-15)
    * Czech uses [ISO-8859-2 encoding](https://en.wikipedia.org/wiki/ISO/IEC_8859-2)
    * Russian is [transliterated](https://pypi.org/project/transliterate/) from Cyrillic to Latin script automatically
    * Arabic uses UTF-8 and is diacritized with [mishkal](https://github.com/linuxscout/mishkal)
* [eSpeak](http://espeak.sourceforge.net)
    * Supports huge number of languages/locales, but sounds robotic

###  Voice Quality

On the Raspberry Pi, you may need to lower the quality of [Larynx](https://github.com/rhasspy/larynx) and [Glow-Speak](https://github.com/rhasspy/glow-speak) voices to get reasonable response times.

This can by done with the `larynx_quality` setting above (use "medium" or "low"), or by appending the vocoder name to the end of your voice:

```yaml
tts:
  - platform: marytts
    voice:larynx:harvard;low
```

Available quality levels are "high", "medium", and "low".

Note that this only applies to Larynx and Glow-Speak voices.
