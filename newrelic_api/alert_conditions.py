from .base import Resource
from newrelic_api.exceptions import NoEntityException


class AlertConditions(Resource):
    """
    An interface for interacting with the NewRelic Alert Conditions API.
    """
    def list(self, policy_id, page=None):
        """
        This API endpoint returns a paginated list of alert conditions associated with the
        given policy_id.
        This API endpoint returns a paginated list of the alert conditions
        associated with your New Relic account. Alert conditions can be filtered
        by their name, list of IDs, type (application, key_transaction, or
        server) or whether or not policies are archived (defaults to filtering
        archived policies).
        :type policy_id: int
        :param policy_id: Alert policy id
        :type page: int
        :param page: Pagination index
        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results
        ::
            {
                "conditions": [
                    {
                        "id": "integer",
                        "type": "string",
                        "name": "string",
                        "enabled": "boolean",
                        "entities": [
                          "integer"
                        ],
                        "metric": "string",
                        "runbook_url": "string",
                        "terms": [
                          {
                            "duration": "string",
                            "operator": "string",
                            "priority": "string",
                            "threshold": "string",
                            "time_function": "string"
                          }
                        ],
                        "user_defined": {
                          "metric": "string",
                          "value_function": "string"
                        }
                    }
                ]
            }
        """
        filters = [
            'policy_id={0}'.format(policy_id),
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}alerts_conditions.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def update(
            self, policy_id, alert_condition_id,
            type=None,
            name=None,
            enabled=None,
            entities=None,
            metric=None,
            runbook_url=None,
            terms=None,
            user_defined=None,
            condition_scope=None):
        """
        Updates any of the optional parameters of the alert condition
        :type policy_id: int
        :param policy_id: Alert policy id where target alert condition belongs to
        :type alert_condition_id: int
        :param alert_condition_id: Alerts condition id to update
        :type name: str
        :param name: The name of the server
        :type enabled: bool
        :param enabled: Whether to enable that alert condition
        :type entities: list[str]
        :param name: entity ids to which the alert condition is applied
        :rtype: dict
        :return: The JSON response of the API
        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NoEntityException>`
            if target alert condition is not included in target policy
        ::
            {
                "condition": {
                    "id": "integer",
                    "type": "string",
                    "name": "string",
                    "enabled": "boolean",
                    "entities": [
                        "integer"
                    ],
                    "metric": "string",
                    "runbook_url": "string",
                    "terms": [
                        {
                            "duration": "string",
                            "operator": "string",
                            "priority": "string",
                            "threshold": "string",
                            "time_function": "string"
                        }
                    ],
                    "user_defined": {
                        "metric": "string",
                        "value_function": "string"
                    }
                }
            }
        """
        conditions_dict = self.list(policy_id)
        target_condition = None
        for condition in conditions_dict['conditions']:
            if int(condition['id']) == alert_condition_id:
                target_condition = condition
                break

        if target_condition is None:
            raise NoEntityException(
                'Target alert condition is not included in that policy.'
                'policy_id: {}, alert_condition_id {}'.format(policy_id, alert_condition_id))

        data = {
            'condition': {
                'type': type or target_condition['type'],
                'name': name or target_condition['name'],
                'enabled': enabled or target_condition['enabled'],
                'entities': entities or target_condition['entities'],
                'metric': metric or target_condition['metric'],
                'runbook_url': runbook_url or target_condition['runbook_url'],
                'terms': terms or target_condition['terms'],
                'user_defined': user_defined or target_condition['user_defined'],
                'condition_scope': condition_scope or target_condition['condition_scope']
            }
        }

        return self._put(
            url='{0}alerts_conditions/{1}.json'.format(self.URL, alert_condition_id),
            headers=self.headers,
            data=data
        )

    def create(self, policy_id, type, name, enabled, entities, metric, runbook_url, terms, user_defined, condition_scope):
        data = {
            'condition': {
                'type': type,
                'name': name,
                'enabled': enabled,
                'entities': entities,
                'metric': metric,
                'runbook_url': runbook_url,
                'terms': terms,
                'user_defined': user_defined,
                'condition_scope': condition_scope
            }
        }

        return self._post(
            url='{0}alerts_conditions/policies/{1}.json'.format(self.URL, policy_id),
            headers=self.headers,
            data=data
        )
        
    def delete(self, condition_id):
        return self._delete(
            url='{0}alerts_conditions/{1}.json'.format(self.URL, condition_id),
            headers=self.headers
        )

        # See https://docs.newrelic.com/docs/alerts/new-relic-alerts-beta/getting-started/rest-api-calls-new-relic-alerts
