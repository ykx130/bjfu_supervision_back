class User(object):
    def __init__(self):
        self.model={
            'name': None,
            'information': {
                'birth': None,
                'sex': None
            },
            'events': [],
            'using': True
        }
        self.events= list()

    @property
    def id(self):
        return self.model['id']


    @id.setter
    def id(self, id_data):
        self.model['id'] = id_data

    @property
    def name(self):
        return self.model['name']

    @name.setter
    def name(self, name_data):
        self.model['name'] = name_data

    @property
    def information(self):
        return self.model['information']

    @information.setter
    def information(self, information_data):
        self.model['information'] = information_data

    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data

    def items_to_dict(self):
        for id, data in enumerate(self.events):
            try:
                data.event_id = id
                self.model['events'].append(data.model)
            except:
                pass


class Event(object):
    def __init__(self):
        self.model = {
            'event_id': None,
            'time': None,
            'value': None,
            'discripe': None,
            'event_using': True
        }

    @property
    def event_id(self):
        return self.model['event_id']

    @event_id.setter
    def event_id(self, event_id_data):
        self.model['event_id'] = event_id_data

    @property
    def time(self):
        return self.model['time']

    @time.setter
    def time(self, time_data):
        self.model['time'] = time_data

    @property
    def value(self):
        return self.model['value']

    @value.setter
    def value(self, value_data):
        self.model['value'] = value_data

    @property
    def discripe(self):
        return self.model['discripe']

    @discripe.setter
    def discripe(self, discripe_data):
        self.model['discripe'] = discripe_data

    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data