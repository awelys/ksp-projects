# Вспомогательная функция для разбора аргумента --items.

def parse_items_arg(items_str):
    """Формат: '1:2,5:1,7:3' -> {1: 2, 5: 1, 7: 3}"""
    result = {}
    if not items_str:
        raise ValueError("Аргумент --items пустой")

    parts = [p.strip() for p in items_str.split(",") if p.strip()]
    for p in parts:
        try:
            mid_str, qty_str = p.split(":")
            mid = int(mid_str)
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            raise ValueError(
                "Неверный формат '%s'. Ожидается menu_id:qty, например '1:2'" % p
            )
        if mid in result:
            result[mid] += qty
        else:
            result[mid] = qty

    if not result:
        raise ValueError("Не удалось разобрать ни одной позиции из --items")
    return result
