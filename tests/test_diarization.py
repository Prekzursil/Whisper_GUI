import pytest

from modules.whisper.data_classes import WhisperImpl
from test_config import is_cuda_available, download_file
from test_transcription import run_asr_pipeline


@pytest.mark.skipif(
    not is_cuda_available(),
    reason="Skipping because the test only works on GPU"
)
@pytest.mark.parametrize(
    "whisper_type,vad_filter,bgm_separation,diarization",
    [
        (WhisperImpl.WHISPER.value, False, False, True),
        (WhisperImpl.FASTER_WHISPER.value, False, False, True),
        (WhisperImpl.INSANELY_FAST_WHISPER.value, False, False, True)
    ]
)
def test_diarization_pipeline(
    whisper_type: str,
    vad_filter: bool,
    bgm_separation: bool,
    diarization: bool,
):
    run_asr_pipeline(whisper_type, vad_filter, bgm_separation, diarization)

