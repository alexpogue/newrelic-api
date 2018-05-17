from .base import Resource


class AlertPolicies(Resource):
    """
    An interface for interacting with the NewRelic Alert Policies API.
    """
    def list(self, filter_name=None, page=None):
        """
        This API endpoint returns a paginated list of the alert policies
        associated with your New Relic account. Alert policies can be filtered
        by their name with exact match.
        :type filter_name: str
        :param filter_name: Filter by name
        :type page: int
        :param page: Pagination index
        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results
        ::
            {
                "policies": [
                    {
                        "id": "integer",
                        "rollup_strategy": "string",
                        "name": "string",
                        "created_at": "integer",
                    },
                ]
            }
        """
        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}alerts_policies.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def create(self, name, incident_preference):
        data = {
            "policy": {
                "name": name,
                "incident_preference": incident_preference
            }
        }

        return self._post(
            url='{0}alerts_policies.json'.format(self.URL),
            headers=self.headers,
            data=data
        )

    def update(self, policy_id, name, incident_preference):
        policies_dict = self.list()
        target_policy = next((p for p in policies_dict['policies'] if int(p['id']) == policy_id), None)
        if target_policy is None:
            raise NoEntityException(
                'Target policy does not exist.'
                'policy_id: {}'.format(policy_id))

        data = {
            'policy': {
                'name': name or target_policy['name'],
                'incident_preference': incident_preference or target_policy['incident_preference']
            }
        }

        return self._put(
            url='{0}alerts_policies/{1}.json'.format(self.URL, policy_id),
            headers=self.headers,
            data=data
        )

    def delete(self, policy_id):
        return self._delete(
            url='{0}alerts_policies/{1}.json'.format(self.URL, policy_id),
            headers=self.headers
        )
