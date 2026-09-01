from ...config import config


def shop_mode():
    mode = config.get("daily_sales_mode")
    if mode is not None:
        return mode
    return "all" if config.get("daily_sales_buy") else "off"
