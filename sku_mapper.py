import re
import logging

class SKUMapper:
    def __init__(self, mapping_df):
        self.map = dict(zip(mapping_df.SKU.str.upper(), mapping_df.MSKU))
        logging.basicConfig(level=logging.INFO)

    def validate_sku(self, sku):
        return bool(re.match(r"^[A-Z0-9\-]+$", sku.strip().upper()))

    def map_sku(self, sku):
        sku_u = sku.strip().upper()
        if not self.validate_sku(sku_u):
            logging.warning(f"Invalid SKU format: {sku}")
            return None
        msku = self.map.get(sku_u)
        if msku is None:
            logging.error(f"No mapping found for {sku}")
        return msku
