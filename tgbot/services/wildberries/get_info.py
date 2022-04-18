import logging

from aiohttp import ClientSession

from tgbot.misc.const import WB_API_URL


logger = logging.getLogger(__name__)


async def get_product_info(vendore_code: str, client_session: ClientSession, user_id: int):
    try:
        async with client_session.get(WB_API_URL + vendore_code) as response:
            if response.status != 200:
                return
            
            json = await response.json(content_type=None)
        
        product = json['data']['products'][0]
        
        wbrand = product['brand']
        wname = product['name']
        wprice = int(product['salePriceU']) // 100
        wsizes = product['sizes']
        
        sizes = list()
        
        if wsizes:
            for size in wsizes:
                sizes.append((size['origName'], size['optionId'], size['stocks']))
        
        
        return wbrand, wname, wprice, sizes
    except IndexError:
        logger.error(f"User [ID:{user_id}]: enter incorrect data")