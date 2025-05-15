# event_manager.py
class EventManager:
    _subscriptions = {}  # Dicionário de eventos e callbacks

    @classmethod
    def subscribe(cls, event_type, callback):
        """Inscreve uma função para ser chamada quando um evento ocorrer."""
        if event_type not in cls._subscriptions:
            cls._subscriptions[event_type] = []
        cls._subscriptions[event_type].append(callback)

    @classmethod
    def publish(cls, event_type, data=None):
        """Dispara um evento e notifica todos os inscritos."""
        for callback in cls._subscriptions.get(event_type, []):
            callback(data)  # Chama a função registrada