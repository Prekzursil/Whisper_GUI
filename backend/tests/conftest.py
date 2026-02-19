import torchaudio


if not hasattr(torchaudio, "AudioMetaData"):
    try:
        from torchaudio._backend.common import AudioMetaData  # type: ignore[attr-defined]
    except Exception:
        class AudioMetaData:  # pragma: no cover
            pass

    torchaudio.AudioMetaData = AudioMetaData  # type: ignore[attr-defined]
