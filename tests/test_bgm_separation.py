import pytest

from modules.whisper.data_classes import WhisperImpl
from test_config import is_cuda_available
from test_transcription import run_asr_pipeline


@pytest.mark.skipif(
    not is_cuda_available(),
    reason="Skipping because the test only works on GPU"
)
@pytest.mark.parametrize(
    "whisper_type,vad_filter,bgm_separation,diarization",
    [
        (WhisperImpl.WHISPER.value, False, True, False),
        (WhisperImpl.FASTER_WHISPER.value, False, True, False),
        (WhisperImpl.INSANELY_FAST_WHISPER.value, False, True, False)
    ]
)
def test_bgm_separation_pipeline(
    whisper_type: str,
    vad_filter: bool,
    bgm_separation: bool,
    diarization: bool,
):
    run_asr_pipeline(whisper_type, vad_filter, bgm_separation, diarization)


@pytest.mark.skipif(
    not is_cuda_available(),
    reason="Skipping because the test only works on GPU"
)
@pytest.mark.parametrize(
    "whisper_type,vad_filter,bgm_separation,diarization",
    [
        (WhisperImpl.WHISPER.value, True, True, False),
        (WhisperImpl.FASTER_WHISPER.value, True, True, False),
        (WhisperImpl.INSANELY_FAST_WHISPER.value, True, True, False)
    ]
)
def test_bgm_separation_with_vad_pipeline(
    whisper_type: str,
    vad_filter: bool,
    bgm_separation: bool,
    diarization: bool,
):
    run_asr_pipeline(whisper_type, vad_filter, bgm_separation, diarization)

