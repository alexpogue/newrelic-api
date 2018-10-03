from .base import Resource


class NotificationChannels(Resource):
    """
    An interface for interacting with the NewRelic Notification Channels API.
    """
    def list(self, page=None):
        """
        This API endpoint returns a paginated list of the notification channels
        associated with your New Relic account.

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results
        """
        filters = [
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{0}alerts_channels.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def update(
            self,
            channel_id,
            name=None,
            type=None,
            configuration=None):
        """
        Updates any of the optional parameters of the notification channel

        :type channel_id: int
        :param channel_id: The id of the channel

        :type type: str
        :param type: The type of notification, e.g. user, email, webhook

        :type configuration: hash
        :param configuration: The configuration for notification

        ::

            {
                "channels": {
                    "id": "integer",
                    "name": "string",
                    "type": "string",
                    "configuration": { }
                }
            }

        """
        channels_dict = self.list()

        target_channel = None

        for channel in channels_dict['channels']
            if int(channel['id'] == channel_id:
                target_channel = channel
                break

        if target_channel is None:
            raise NoEntityException(
                'Target notification channel does not exist.'
                'channel_id {}'.format(channel_id)
            )

        data = {
            'channel': {
                'name': name or target_condition['name'],
                'type': type or target_condition['type'],
                'configuration': configuration or target_condition['configuration']
            }

        return self._put(
            url='{0}alerts_channels/{1}.json'.format(self.URL, channel_id),
            headers=self.headers,
            data=data
        )

    def create(self, name, type, configuration):
        """
        This API endpoint allows you to create a notification channel, see
            New Relic API docs for details of types and configuration

        :type name: str
        :param name: The name of the channel

        :type type: str
        :param type: Type of notification, eg. email, user, webhook

        :type configuration: hash
        :param configuration: Configuration for notification

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "channels": {
                     "id": "integer",
                     "name": "string",
                     "type": "string",
                     "configuration": { },
                     "links": {
                        "policy_ids": []
                    }
                }
            }

        """

        data = {
            "channel": {
                "name": name,
                "type": type,
                "configuration": configuration
            }
        }

        return self._post(
            url='{0}alerts_channels.json'.format(self.URL),
            headers=self.headers,
            data=data
        )

    def delete(self, id):
        """
        This API endpoint allows you to delete a notification channel

        :type id: integer
        :param id: The id of the channel

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "channels": {
                     "id": "integer",
                     "name": "string",
                     "type": "string",
                     "configuration": { },
                     "links": {
                        "policy_ids": []
                    }
                }
            }

        """

        return self._delete(
            url='{0}alerts_channels/{1}.json'.format(self.URL, id),
            headers=self.headers
        )
