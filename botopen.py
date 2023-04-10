import vk_api
from configuration import user_token
from vk_api.exceptions import ApiError

class VkTools():
    def __init__(self, token):
        self.exist_api = vk_api.VkApi(token=token)

    def get_profile_info(self, user_id):

        try:
            info = self.exist_api.method('users.get',
                                       {'user_id': user_id,
                                        'fields': 'bdate,city,sex'
                                        }
                                      )
        except ApiError:
            return

        return info

        def user_search(self, city_id, age_from, age_to, sex, offset=None):

            try:
                profiles = self.exist_api.method('users.search',
                                               {'city_id': city_id,
                                                'age_from': age_from,
                                                'age_to': age_to,
                                                'sex': sex,
                                                'count': 30,
                                                'offset': offset
                                                })

            except ApiError:
                return

            profiles = profiles['items']

            final_result = []
            for profile in profiles:
                if profile['is_closed'] == False:
                    final_result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                                   'id': profile['id']
                                   })

            return final_result

        def photos_get(self, user_id):
            global top3
            photos = self.exist_api.method('photos.get',
                                         {'album_id': 'profile',
                                          'owner_id': user_id
                                          }
                                         )
            try:
                photos = photos['items']
            except KeyError:
                return

            final_result = []
            for num, photo in enumerate(photos):
                final_result.append({'owner_id': photo['owner_id'],
                               'id': photo['id'],
                               'hype': sum(photo['likes'], photo['comments'])
                               })
            for hype in final_result:
                top3 = sorted(final_result, key=hype.get, reverse=True)[:3]

            return top3



if __name__ == '__main__':
    tools = VkTools(user_token)
    photos = tools.photos_get()
    print(photos)