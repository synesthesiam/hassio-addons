# OpenTTS (de)

Unifies access to multiple open source text to speech systems and voices for many languages.

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
    * Default is "high", choices are "high", "medium", "low"
* `larynx_denoiser_strength`
    * Amount to apply denoiser during [Larynx TTS](https://github.com/rhasspy/larynx) post-processing
    * Default is 0.001 (higher value reduces noise, but distorts voice)
* `larynx_noise_scale`
    * Volatility of [Larynx TTS](https://github.com/rhasspy/larynx) vocalization
    * Default is 0.333, range is 0-1. Higher values make the voice less monotone
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
    voice:larynx:harvard-glow_tts
```

The `voice` format is `<TTS_SYSTEM>:<VOICE_NAME>`. Visit the OpenTTS web UI and copy/paste the "voice id" of your favorite voice here.

You may leave out the `port` setting if you configure the OpenTTS host port to be 59125 instead of 5500.

## Supported Text to Speech Systems

Below is a list of the supported TTS systems and voice counts by language.

* [Larynx](https://github.com/rhasspy/larynx-runtime)
    * English (21), German (5), French (3), Spanish (2), Dutch (3), Russian (3), Swedish (1), Italian (2)
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

### Larynx Voice Quality

On the Raspberry Pi, you may need to lower the quality of [Larynx](https://github.com/rhasspy/larynx) voices to get reasonable response times.

This can by done with the `larynx_quality` setting above (use "medium" or "low"), or by appending the vocoder name to the end of your voice:

```yaml
tts:
  - platform: marytts
    voice:larynx:harvard-glow_tts;hifi_gan:vctk_small
```

Available vocoders are:

* `hifi_gan:universal_large` (best quality, slowest, default)
* `hifi_gan:vctk_medium` (medium quality)
* `hifi_gan:vctk_small` (lowest quality, fastest)

Note that this only applies to Larynx voices.
