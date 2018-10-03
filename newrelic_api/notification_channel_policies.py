from .base import Resource

class NotificationChannelPolicies(Resource):
    """
    An interface for interacting with the NewRelic Notification Channel Policies
    API.
    """

    def update(self, policy_id, channel_ids):
        """
        Updates the list of Notification Channel ids the policy refers to

        :type policy_id: int
        :param policy_id: The id of the policy

        :type channel_ids: list
        :param channel_ids: List of channels to set the policy to refer to

        ::

        {
            "policy_channels": {
                "policy_id": "integer",
                "channel_ids": [ ]
            }
        }

        """

        params = [
            'policy_id={}'.format(policy_id),
            'channel_ids={}'.format(','.join(str(x) for x in channel_ids))
        ]

        return self._put(
            url='{0}alerts_policy_channels.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(params)
        )

    def delete(self, channel_id, policy_id):
        """
        Deletes the association between the notification channel and the policy

        :type channel_id: int
        :param channel_id: The id of the Notification Channel

        :type policy_id: int
        :param policy_id: The id of the policy

        ::

        {
            "policy_channels": {
                "policy_id": "integer",
                "channel_ids": [ ]
            }
        }

        """
    params = [ 
        'channel_id={}'.format(channel_id),
        'policy_id={}'.format(policy_id)
    ]

    return self._delete(
        url='{0}alerts_policy_channels.json'.format(self.URL),
        headers=self.headers,
        params=self.build_param_string(params)
    )
