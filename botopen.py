from pprint import pprint
from datetime import datetime

import vk_api
from configuration import user_token
from vk_api.exceptions import ApiError


class VkTools:

    def __init__(self, user_token):
        self.exist_api = vk_api.VkApi(token=user_token)

    def year_bdate(self, bdate):
        year_user = bdate.split('.')[2]
        now = datetime.now().year
        return now - int(year_user)

    def get_profile_info(self, user_id):

        try:
            info, = self.exist_api.method('users.get',
                                          {'user_id': user_id,
                                           'fields': 'bdate,city,sex'
                                           }
                                          )
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        result_final = {'name': (info['first_name'] + ' ' + info['last_name']) if
                        'first_name' in info and 'last_name' in info else None,
                        'sex': info.get('sex'),
                        'city': info.get('city')['title'] if info.get('city') is not None else None,
                        'year': self.year_bdate(info.get('bdate'))
                        }
        return result_final

    def user_search(self, params, offset=0):

        try:
            profiles = self.exist_api.method('users.search',
                                             {
                                                 'home_town': params['city'],
                                                 'age_from': params['year'] - 3,
                                                 'age_to': params['year'] + 3,
                                                 'sex': 1 if params['sex'] == 2 else 2,
                                                 'count': 10,
                                                 'offset': offset,
                                                 'has_photo': True
                                             }
                                             )

        except ApiError as e:
            profiles = []
            print(f'error = {e}')

        result_now = [{'name': item['first_name'] + item['last_name'],
                       'id': item['id']
                       } for item in profiles if item['is_closed'] is False
                      ]

        return result_now

    def photos_get(self, id):
        try:
            photos = self.exist_api.method('photos.get',
                                           {'album_id': 'profile',
                                            'owner_id': id,
                                            'extended': 1
                                            }
                                           )
        except ApiError as e:
            photos = {}
            print(f'error = {e}')

        return photos

        final_result = []
        for num, photo in enumerate(photos):
            final_result.append({'owner_id': photo['owner_id'],
                                 'id': photo['id'],
                                 'likes': photo['likes']['count'],
                                 'comments': photo['comments']['count']
                                 })
        final_result = sorted(final_result, key=lambda x: x['likes']['count'], reverse=True)
        if len(final_result) > 3:
            final_result = final_result[:3]
        return final_result


if __name__ == '__main__':
    tools = VkTools(user_token)
    params = tools.get_profile_info('user_id')
    worksheets = tools.user_search(params)
    worksheet = worksheets.pop()
    photos = tools.photos_get(worksheet['id'])

    pprint(worksheets)
