import re

def validate_duration_format(text):
    """Проверка корректности: только цифры (целые или дробные)."""
    pattern = r'^\d+([.,]\d{1,2})?$'
    return bool(re.match(pattern, text))

def clean_text(text):
    """Анализ и очистка: удаляем всё, кроме букв и пробелов, убираем лишние пробелы."""
    # Регулярка [^a-zA-Zа-яА-ЯёЁ\s] находит всё, что НЕ является буквой или пробелом
    cleaned = re.sub(r'[^a-zA-Zа-яА-ЯёЁ\s]', '', text)
    # Убираем двойные пробелы и пробелы по краям
    return re.sub(r'\s+', ' ', cleaned).strip().capitalize()