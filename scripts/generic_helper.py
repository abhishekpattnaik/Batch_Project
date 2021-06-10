# from django.db.models import base
from django.db.models import query
from batch_app.models import Batch, Code
import string, random
from constants.constant import ALPHANUMERICLEN, sample_paginated_response
from concurrent.futures import ThreadPoolExecutor
import uuid

def get_paginated_response(request, query_set, pn):
    if not query_set:
        return {}
    page_number = int(pn)

    if page_number <= 0:
        page_number = 1
    
    paginated_response = sample_paginated_response.copy()
    page_limit = paginated_response['page_size']
    request_url = request.build_absolute_uri()
    # import pdb;pdb.set_trace()
    search_word = request.GET.get('search_keyword')

    base_url = request_url.split('?')[0]
    base_url = base_url + '?search_keyword={}'.format(search_word)
    # total_pages = paginated_response['count']/page_limit
    next_str = '&page={}'.format(str(page_number+1))
    previous_str = '&page={}'.format(str(page_number-1))
    paginated_response['page_footer'] = 'Page {}/{}'.format(str(page_number),str(query_set.count()//page_limit))
    paginated_response['count'] = query_set.count()
    paginated_response['next'] = base_url + next_str
    paginated_response['previous'] = base_url + previous_str
    paginated_response['data'] = query_set[(page_number - 1) * page_limit:((page_number - 1) * page_limit)+page_limit]
    return paginated_response

def generate_code(length, batch):
    for _ in range(length):
        yield Code(batch = batch,batch_code = uuid.uuid4().hex[:ALPHANUMERICLEN])

def create_data(user, batch_name, number_of_codes):
    batch, _ = Batch.objects.get_or_create(batch_user = user, name = batch_name)
    bulk_update_list = generate_code(number_of_codes, batch = batch)
    codes = Code.objects.bulk_create(bulk_update_list)
    return codes, True