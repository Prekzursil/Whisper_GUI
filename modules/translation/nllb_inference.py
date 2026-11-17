from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import gradio as gr
import os

from modules.utils.paths import TRANSLATION_OUTPUT_DIR, NLLB_MODELS_DIR
from modules.translation.translation_base import TranslationBase
from modules.translation.nllb_langs import NLLB_AVAILABLE_LANGS


class NLLBInference(TranslationBase):
    def __init__(self,
                 model_dir: str = NLLB_MODELS_DIR,
                 output_dir: str = TRANSLATION_OUTPUT_DIR
                 ):
        super().__init__(
            model_dir=model_dir,
            output_dir=output_dir
        )
        self.tokenizer = None
        self.available_models = ["facebook/nllb-200-3.3B", "facebook/nllb-200-1.3B", "facebook/nllb-200-distilled-600M"]
        self.available_source_langs = list(NLLB_AVAILABLE_LANGS.keys())
        self.available_target_langs = list(NLLB_AVAILABLE_LANGS.keys())
        self.pipeline = None

    def translate(self,
                  text: str,
                  max_length: int
                  ):
        result = self.pipeline(
            text,
            max_length=max_length
        )
        return result[0]["translation_text"]

    def update_model(self,
                     model_size: str,
                     src_lang: str,
                     tgt_lang: str,
                     progress: gr.Progress = gr.Progress()
                     ):
        def validate_language(lang: str) -> str:
            if lang in NLLB_AVAILABLE_LANGS:
                return NLLB_AVAILABLE_LANGS[lang]
            elif lang not in NLLB_AVAILABLE_LANGS.values():
                raise ValueError(f"Language '{lang}' is not supported. Use one of: {list(NLLB_AVAILABLE_LANGS.keys())}")
            return lang

        src_lang = validate_language(src_lang)
        tgt_lang = validate_language(tgt_lang)

        if model_size != self.current_model_size or self.model is None:
            print("\nInitializing NLLB Model..\n")
            progress(0, desc="Initializing NLLB Model..")
            self.current_model_size = model_size
            local_files_only = self.is_model_exists(self.current_model_size)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name_or_path=model_size,
                                                               cache_dir=self.model_dir,
                                                               local_files_only=local_files_only)
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_size,
                                                           cache_dir=os.path.join(self.model_dir, "tokenizers"),
                                                           local_files_only=local_files_only)

        self.pipeline = pipeline("translation",
                                 model=self.model,
                                 tokenizer=self.tokenizer,
                                 src_lang=src_lang,
                                 tgt_lang=tgt_lang,
                                 device=self.device)

    def is_model_exists(self,
                        model_size: str):
        """Check if model exists or not (Only facebook model)"""
        prefix = "models--facebook--"
        _id, model_size_name = model_size.split("/")
        model_dir_name = prefix + model_size_name
        model_dir_path = os.path.join(self.model_dir, model_dir_name)
        if os.path.exists(model_dir_path) and os.listdir(model_dir_path):
            return True
        for model_dir_name in os.listdir(self.model_dir):
            if (model_size in model_dir_name or model_size_name in model_dir_name) and \
                    os.listdir(os.path.join(self.model_dir, model_dir_name)):
                return True
        return False


