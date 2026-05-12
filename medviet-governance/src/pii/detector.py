# src/pii/detector.py
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider

def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có 12 chữ số (có thể mất số 0 đầu khi đọc CSV)
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\b\d{10,12}\b",
        score=0.9
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        patterns=[cccd_pattern],
        context=["cccd", "căn cước", "chứng minh", "cmnd"],
        supported_language="vi"
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (có thể mất số 0 đầu)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"\b0?[35789]\d{8}\b",
            score=0.85
        )],
        context=["điện thoại", "sdt", "phone", "liên hệ"],
        supported_language="vi"
    )

    # --- TASK 2.2.5 ---
    # Tạo PERSON recognizer cho tiếng Việt (do spacy model có thể thiếu NER)
    # Pattern: Các từ viết hoa chữ cái đầu, có từ 2-5 từ
    # Đã bổ sung đầy đủ các ký tự tiếng Việt có dấu
    VN_CAPS = "A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỤỦỨỪỬỮỰỲỴỶỸ"
    VN_LOW = "a-zàáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậẹẻẽếềểễệỉịọỏốồổỗộụủứừửữựỳỵỷỹ"
    
    name_pattern = Pattern(
        name="vn_name_pattern",
        regex=rf"\b[{VN_CAPS}][{VN_LOW}]*(\s[{VN_CAPS}][{VN_LOW}]*){{1,4}}\b",
        score=0.8
    )
    person_recognizer = PatternRecognizer(
        supported_entity="PERSON",
        patterns=[name_pattern],
        supported_language="vi"
    )

    # Đảm bảo EmailRecognizer hỗ trợ 'vi'
    from presidio_analyzer.predefined_recognizers import EmailRecognizer
    email_recognizer = EmailRecognizer(supported_language="vi")

    # --- TASK 2.2.3 ---
    # Tạo NLP engine dùng spaCy Vietnamese model
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", 
                    "model_name": "vi_core_news_lg"}]
    })
    nlp_engine = provider.create_engine()

    # --- TASK 2.2.4 ---
    # Khởi tạo AnalyzerEngine và add các recognizer
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine, 
        default_score_threshold=0.4,
        supported_languages=["vi", "en"]
    )
    analyzer.registry.add_recognizer(cccd_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)
    analyzer.registry.add_recognizer(person_recognizer)
    analyzer.registry.add_recognizer(email_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,
        language="vi",
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
    return results
